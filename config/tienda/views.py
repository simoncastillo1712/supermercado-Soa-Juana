from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models.deletion import RestrictedError
from django.db import IntegrityError
import json

from .models import Categoria, Producto, Cliente, Proveedor
from .forms import CategoriaForm, ProductoForm, ClienteForm, ProveedorForm

#####################################
# VISTAS PUBLICAS
#####################################

def inicio(request):
    productos_destacados = Producto.objects.all()[:4]  # O filtro los más vendidos si tienes campo
    cat_q = request.GET.get('cat_q', '').strip()

    categorias_qs = Categoria.objects.all()
    if cat_q:
        categorias_qs = categorias_qs.filter(nombre__icontains=cat_q)

    categorias = categorias_qs[:10]

    contexto = {
        'productos_destacados': productos_destacados,
        'categorias': categorias,
        'cat_q': cat_q,
    }
    return render(request, 'inicio.html', contexto)

def listar_productos(request):
    q = request.GET.get('q', '')
    productos = Producto.objects.select_related('id_categoria')
    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(id_categoria__nombre__icontains=q)
        )
    else:
        productos = productos.all()

    carrito = request.session.get('carrito', {})
    carrito_total_items = sum(int(cantidad) for cantidad in carrito.values())

    contexto = {
        'productos': productos,
        'carrito_total_items': carrito_total_items,
        'q': q,
    }
    return render(request, 'productos/listar.html', contexto)

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0

    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id_producto=producto_id)
            subtotal = producto.precio * cantidad
            total += subtotal
            items.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal,
            })
        except Producto.DoesNotExist:
            continue

    carrito_total_items = sum(int(cantidad) for cantidad in carrito.values())

    contexto = {
        'items': items,
        'total': total,
        'carrito_total_items': carrito_total_items,
    }
    return render(request, 'carrito/ver.html', contexto)

@require_POST
def agregar_al_carrito(request):
    try:
        data = json.loads(request.body)
        producto_id = str(data.get('producto_id'))
        cantidad = int(data.get('cantidad', 1))
    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse({'ok': False, 'mensaje': 'Datos inválidos.'}, status=400)

    if cantidad < 1 or cantidad > 5:
        return JsonResponse({'ok': False, 'mensaje': 'Cantidad inválida (1 a 5).'}, status=400)

    producto = get_object_or_404(Producto, id_producto=producto_id)

    carrito = request.session.get('carrito', {})
    cantidad_actual = int(carrito.get(producto_id, 0))
    nueva_cantidad = cantidad_actual + cantidad

    if nueva_cantidad > 5:
        nueva_cantidad = 5

    carrito[producto_id] = nueva_cantidad
    request.session['carrito'] = carrito
    request.session.modified = True

    total_items_carrito = sum(int(cantidad) for cantidad in carrito.values())

    return JsonResponse({
        'ok': True,
        'mensaje': f'{producto.nombre} agregado al carrito.',
        'cantidad_en_carrito': nueva_cantidad,
        'total_items_carrito': total_items_carrito,
    })

@require_POST
def eliminar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    producto_id = str(id)

    if producto_id in carrito:
        del carrito[producto_id]
        request.session['carrito'] = carrito
        request.session.modified = True

    return redirect('ver_carrito')

@require_POST
def vaciar_carrito(request):
    request.session['carrito'] = {}
    request.session.modified = True
    return redirect('ver_carrito')


#####################################
# AUTENTICACION
#####################################

def login_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('inicio')
        
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('inicio')

#####################################
#  GESTION DE LAS CATEGORIAS
#####################################

@login_required
def listar_categorias(request):
    q = request.GET.get('q', '')
    if q:
        categorias = Categoria.objects.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q)
        )
    else:
        categorias = Categoria.objects.all()
    contexto = {
        'categorias': categorias,
        'q': q
    }
    return render(request, 'categorias/listar.html', contexto)

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada correctamente.')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    
    contexto = {
        'form':form
    }
    
    return render(request, 'categorias/form.html', contexto)

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id_categoria=id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" actualizada correctamente.')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    contexto = {
        'form':form
    }
    
    return render(request, 'categorias/form.html', contexto)
    
    
@login_required
@require_POST
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id_categoria=id)
    try:
        categoria.delete()
        messages.success(request, f'Categoría "{categoria.nombre}" eliminada correctamente.')
    except IntegrityError:
        messages.error(
            request,
            f'No se puede eliminar la categoría "{categoria.nombre}" porque tiene productos asociados.'
        )
    except Exception:
        messages.error(request, 'Ocurrió un error inesperado al intentar eliminar la categoría.')
    return redirect('listar_categorias')
  
#####################################
#  GESTION DE PRODUCTOS
#####################################

@login_required
def listar_productos_admin(request):
    q = request.GET.get('q', '')
    productos = Producto.objects.select_related('id_categoria')
    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(id_categoria__nombre__icontains=q)
        )
    else:
        productos = productos.all()
    contexto = {
        'productos': productos,
        'q': q
    }
    return render(request, 'productos/listar_admin.html', contexto)

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado correctamente.')
            return redirect('listar_productos_admin')
    else:
        form = ProductoForm()
    
    contexto = {
        'form':form
    }
    
    return render(request, 'productos/form.html', contexto)

@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('listar_productos_admin')
    else:
        form = ProductoForm(instance=producto)
    
    contexto = {
        'form':form
    }
    
    return render(request, 'productos/form.html', contexto)


@login_required
@require_POST
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    try:
        producto.delete()
        messages.success(request, f'Producto "{producto.nombre}" eliminado correctamente.')
    except RestrictedError:
        messages.error(
            request,
            f'No se puede eliminar el producto "{producto.nombre}" porque tiene registros asociados en ventas o compras.'
        )
    except IntegrityError:
        messages.error(
            request,
            f'No se puede eliminar el producto "{producto.nombre}" porque tiene dependencias relacionadas.'
        )
    except Exception:
        messages.error(
            request,
            'Ocurrió un error inesperado al intentar eliminar el producto.'
        )
    return redirect('listar_productos_admin')

#####################################
#  GESTION DE CLIENTES
#####################################

@login_required
def listar_clientes(request):
    q = request.GET.get('q', '')
    if q:
        clientes = Cliente.objects.filter(
            Q(razon_social__icontains=q) | Q(rut_cliente__icontains=q)
        )
    else:
        clientes = Cliente.objects.all()

    # Aquí va paginación que se explicará abajo

    contexto = {
        'clientes': clientes,
        'q': q,
        # 'page_obj': page_obj, si usas paginación
    }
    return render(request, 'clientes/listar.html', contexto)

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        
        if form.is_valid():
            cliente = form.save(commit=False)
            if not cliente.fecha_registro:
                cliente.fecha_registro = timezone.now()
            cliente.save()
            messages.success(request, f'Cliente "{cliente.razon_social}" creado correctamente.')
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    
    contexto = {
        'form':form
    }
    
    return render(request, 'clientes/form.html', contexto)

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id_cliente=id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        
        if form.is_valid():
            cliente = form.save(commit=False)
            if not cliente.fecha_registro:
                cliente.fecha_registro = timezone.now()
            cliente.save()
            messages.success(request, f'Cliente "{cliente.razon_social}" actualizado correctamente.')
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    
    contexto = {
        'form':form
    }
    
    return render(request, 'clientes/form.html', contexto)


@login_required
@require_POST
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id_cliente=id)
    try:
        cliente.delete()
        messages.success(request, f'Cliente "{cliente.razon_social}" eliminado correctamente.')
    except IntegrityError:
        messages.error(
            request,
            f'No se puede eliminar el cliente "{cliente.razon_social}" porque tiene documentos asociados.'
        )
    except Exception:
        messages.error(request, 'Ocurrió un error inesperado al intentar eliminar el cliente.')
    return redirect('listar_clientes')


#####################################
#  GESTION DE PROVEEDORES
#####################################

@login_required
def listar_proveedores(request):
    q = request.GET.get('q', '')
    if q:
        proveedores = Proveedor.objects.filter(
            Q(nombre_proveedor__icontains=q) | Q(rut_proveedor__icontains=q)
        )
    else:
        proveedores = Proveedor.objects.all()
    contexto = {
        'proveedores': proveedores,
        'q': q
    }
    return render(request, 'proveedores/listar.html', contexto)

@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'Proveedor "{proveedor.nombre_proveedor}" creado correctamente.')
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm()
    
    contexto = {
        'form':form
    }
    
    return render(request, 'proveedores/form.html', contexto)

@login_required
def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'Proveedor "{proveedor.nombre_proveedor}" actualizado correctamente.')
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    
    contexto = {
        'form':form
    }
    
    return render(request, 'proveedores/form.html', contexto)


@login_required
@require_POST
def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id)
    try:
        proveedor.delete()
        messages.success(request, f'Proveedor "{proveedor.nombre_proveedor}" eliminado correctamente.')
    except IntegrityError:
        messages.error(
            request,
            f'No se puede eliminar el proveedor "{proveedor.nombre_proveedor}" porque tiene compras asociadas.'
        )
    except Exception:
        messages.error(request, 'Ocurrió un error inesperado al intentar eliminar el proveedor.')
    return redirect('listar_proveedores')
