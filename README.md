**Datos de Admin**

**user: root** / 
**contraseña: 1234**

# Supermercado La Soa Juana.

Aplicación web desarrollada con **Django** para gestión de supermercado, con:
- sitio público para clientes,
- administración interna (categorías, productos, clientes y proveedores),
- carrito de compras en sesión,
- buscadores y mejoras visuales en la página de inicio.

---

## 1) ¿Qué hace este sitio?

El sistema permite operar un supermercado con dos grandes áreas:

### A. Área pública (sin login)
- **Inicio (`/`)**
  - Banner principal.
  - Banner de **delivery** con descuentos por monto de compra.
  - Sección de **productos destacados** con imágenes de los productos.
  - Sección de **categorías**:
    - muestra hasta 10 categorías.
    - incluye barra de búsqueda (`cat_q`) para filtrar categorías en la misma home.
  - Sección de **promociones** con tarjetas visuales.
- **Listado de productos (`/listar_productos`)**
  - Tarjetas de productos con imagen, precio y stock.
  - Búsqueda por nombre de producto o categoría (`q`).
  - Botón “Comprar” (integración con modal/carrito vía JS).
- **Carrito (`/carrito/`)**
  - Muestra productos agregados, cantidades y total.
  - Persistencia en sesión.

### B. Área de gestión interna (requiere autenticación)
- CRUD de:
  - Categorías
  - Productos
  - Clientes
  - Proveedores
- Uso de mensajes de éxito/error en operaciones create/update/delete.
- Pantallas y formularios administrativos en templates por módulo.

---

## 2) Funcionalidades destacadas implementadas

- Corrección de visualización de imágenes en “Productos destacados” de inicio usando la imagen real del producto.
- Mejoras UX/UI en home:
  - banner delivery compacto, centrado.
  - promociones en tarjetas al final de la página.
- Búsqueda en home para categorías (`cat_q`) con límite de 10 resultados.
- Búsqueda pública de productos por texto (`q`).
- Manejo de archivos media para imágenes de productos (`MEDIA_URL` / `MEDIA_ROOT`).

---

## 3) Arquitectura y estructura del proyecto

```text
supermercado/
├─ config/
│  ├─ manage.py
│  ├─ config/                  # configuración Django (settings, urls, wsgi, asgi)
│  ├─ tienda/                  # app principal
│  │  ├─ models.py             # modelos mapeados a BD existente
│  │  ├─ views.py              # vistas públicas y privadas
│  │  ├─ urls.py               # rutas de la app
│  │  ├─ forms.py              # formularios de gestión
│  │  ├─ templates/            # HTML (inicio, productos, carrito, auth, CRUDs)
│  │  └─ static/               # CSS, JS e imágenes estáticas
│  └─ media/                   # imágenes subidas (productos)
├─ TODO.md
└─ README.md
```

---

## 4) Tecnologías usadas

- Python 3.x
- Django 6.0.3
- MySQL (backend de base de datos)
- HTML + CSS + JavaScript
- Bootstrap (clases utilitarias y componentes visuales)

---

## 5) Modelos principales (resumen)

En `config/tienda/models.py` existen modelos mapeados a una BD existente (`managed = False`), entre ellos:

- `Categoria`
- `Producto` (incluye `imagen`, `precio`, `stock`, FK a categoría)
- `Cliente`
- `Proveedor`
- `Compra` / `DetalleCompra`
- `Venta` / `DetalleVenta`
- `Factura` / `Boleta`
- `TablaVistaFactura` (vista de BD)

> Nota: al estar con `managed = False`, Django no administra creación/modificación de tablas por migraciones para esos modelos.

---

## 6) Rutas y navegación (alto nivel)

- `/` → inicio público
- `/listar_productos` → catálogo público con búsqueda
- `/carrito/` → vista de carrito
- rutas de gestión (categorías/productos/clientes/proveedores) definidas en `config/tienda/urls.py`
- autenticación de usuarios para acceso administrativo

---

## 7) Configuración local (paso a paso)

## Requisitos previos
- Python 3.10+ (ideal 3.12/3.13)
- MySQL Server activo
- Base de datos `supermercado` creada y accesible

## 1. Crear y activar entorno virtual
En Windows (CMD):
```bash
python -m venv venv
venv\Scripts\activate
```

## 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 3. Configurar base de datos
En `config/config/settings.py` revisar bloque `DATABASES`:
- ENGINE: `django.db.backends.mysql`
- NAME: `supermercado`
- USER/PASSWORD/HOST/PORT según tu entorno local.

## 4. Ejecutar servidor
```bash
python config/manage.py runserver
```

Sitio disponible en:
- http://127.0.0.1:8000/

---

## 8) Archivos estáticos y media

- `STATIC_URL = 'static/'`
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = BASE_DIR / 'media'`

En desarrollo, `config/config/urls.py` sirve media cuando `DEBUG=True`.

---

## 9) Flujo funcional recomendado para pruebas manuales

1. Abrir `/` y validar:
   - banner principal,
   - banner delivery compacto,
   - productos destacados con imagen,
   - categorías (máximo 10) y barra de búsqueda,
   - tarjetas de promociones.
2. Probar búsqueda de categorías en home:
   - vacío,
   - texto con resultados,
   - texto sin resultados.
3. Abrir `/listar_productos`:
   - buscar productos con `q`,
   - abrir modal/acción de compra.
4. Abrir `/carrito/` y validar totales/items.
5. Probar módulos administrativos con usuario autenticado.

---

## 10) Seguridad y consideraciones importantes

- `SECRET_KEY` no debe exponerse en producción.
- `DEBUG` debe ser `False` en producción.
- Definir `ALLOWED_HOSTS` apropiado para despliegue.
- Usar variables de entorno para credenciales sensibles (BD, secret key).

---

## 11) Estado actual de la UI de inicio

La página de inicio incluye:
- diseño mejorado y secciones visuales consistentes,
- delivery destacado con descuentos por tramos,
- promociones inventadas para atraer conversión,
- categorización y acceso rápido a catálogo.

---

## 12) Posibles mejoras futuras

- Checkout completo con creación formal de ventas/facturas.
- Integración de pasarela de pago.
- Panel analítico (ventas por período, top productos).
- Paginación y filtros avanzados en catálogo público.
- Tests automáticos (`pytest` / `django test`) para vistas y lógica de carrito.
- Internacionalización (`es-CL`) y formato moneda local.

---

## 13) Comandos útiles

```bash
# checks Django
python config/manage.py check

# servidor
python config/manage.py runserver

# crear superusuario (si aplica)
python config/manage.py createsuperuser
```

---

Documentación preparada para dejar el proyecto listo para uso académico/taller y continuación de desarrollo.
