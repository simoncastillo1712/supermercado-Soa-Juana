# TODO - Correcciones Inicio / Categorías

- [x] Actualizar `config/tienda/templates/inicio.html`
  - [x] Hacer que "Comprar" en productos destacados abra el modal de compra (mismo flujo que listado de productos).
  - [x] Corregir links de categorías destacadas para evitar error al hacer clic (redirigir a listado de productos filtrado por categoría).

- [x] Actualizar `config/tienda/static/js/script.js`
  - [x] Permitir que el modal funcione también con tarjetas de inicio (botón comprar y/o click en tarjeta).
  - [x] Asegurar compatibilidad con ambos templates (`productos/listar.html` e `inicio.html`) sin romper la lógica del carrito.

- [x] Verificar consistencia de parámetros de búsqueda
  - [x] Confirmar que inicio use `cat_q` para el buscador local.
  - [x] Confirmar que navegación por categoría use `q` hacia `listar_productos`.
