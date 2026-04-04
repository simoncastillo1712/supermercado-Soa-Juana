document.addEventListener('DOMContentLoaded', function () {
    const productoCards = document.querySelectorAll('.producto-card');
    const modal = document.getElementById('productoModal');
    const cerrarModalBtn = document.getElementById('cerrarModalBtn');
    const seguirComprandoBtn = document.getElementById('seguirComprandoBtn');
    const agregarCarritoBtn = document.getElementById('agregarCarritoBtn');
    const cantidadProducto = document.getElementById('cantidadProducto');
    const modalProductoNombre = document.getElementById('modalProductoNombre');
    const modalProductoPrecio = document.getElementById('modalProductoPrecio');
    const modalProductoStock = document.getElementById('modalProductoStock');
    const modalProductoImagen = document.getElementById('modalProductoImagen');
    const modalFeedback = document.getElementById('modalFeedback');
    const carritoBadge = document.getElementById('carritoBadge');
    let productoSeleccionadoId = null;

    if (!modal) {
        return;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function actualizarBadgeCarrito(totalItems) {
        if (!carritoBadge) return;
        const total = parseInt(totalItems, 10) || 0;
        if (total > 0) {
            carritoBadge.textContent = total;
            carritoBadge.classList.remove('d-none');
        } else {
            carritoBadge.textContent = '0';
            carritoBadge.classList.add('d-none');
        }
    }

    function abrirModal(card) {
        productoSeleccionadoId = card.dataset.id || null;
        modalProductoNombre.textContent = card.dataset.nombre || '';
        modalProductoPrecio.textContent = '$ ' + (card.dataset.precio || '0');
        modalProductoStock.textContent = 'Stock: ' + (card.dataset.stock || '0') + ' UNI';

        if (card.dataset.imagen) {
            modalProductoImagen.src = card.dataset.imagen;
            modalProductoImagen.style.display = 'block';
        } else {
            modalProductoImagen.style.display = 'none';
            modalProductoImagen.removeAttribute('src');
        }

        cantidadProducto.value = '1';
        modalFeedback.textContent = '';
        modal.classList.add('show');
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
    }

    function cerrarModal() {
        modal.classList.remove('show');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    productoCards.forEach(function (card) {
        const botonComprar = card.querySelector('.btn-comprar');
        if (botonComprar) {
            botonComprar.addEventListener('click', function (event) {
                event.preventDefault();
                event.stopPropagation();
                abrirModal(card);
            });
        }
    });

    if (cerrarModalBtn) cerrarModalBtn.addEventListener('click', cerrarModal);
    if (seguirComprandoBtn) seguirComprandoBtn.addEventListener('click', cerrarModal);

    if (modal) {
        modal.addEventListener('click', function (event) {
            if (event.target === modal) cerrarModal();
        });
    }

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && modal.getAttribute('aria-hidden') === 'false') {
            cerrarModal();
        }
    });

    if (agregarCarritoBtn) {
        agregarCarritoBtn.addEventListener('click', function () {
            const cantidad = parseInt(cantidadProducto.value, 10);
            if (isNaN(cantidad) || cantidad < 1 || cantidad > 5) {
                modalFeedback.textContent = 'La cantidad debe estar entre 1 y 5.';
                modalFeedback.style.color = '#dc3545';
                return;
            }

            if (!productoSeleccionadoId) {
                modalFeedback.textContent = 'No se pudo identificar el producto.';
                modalFeedback.style.color = '#dc3545';
                return;
            }

            fetch('/carrito/agregar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    producto_id: productoSeleccionadoId,
                    cantidad: cantidad
                })
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        return { ok: response.ok, data: data };
                    });
                })
                .then(function (result) {
                    if (!result.ok || !result.data.ok) {
                        throw new Error(result.data.mensaje || 'No fue posible agregar al carrito.');
                    }
                    modalFeedback.textContent = result.data.mensaje + ' (' + cantidad + ' unidad(es))';
                    modalFeedback.style.color = '#198754';
                    actualizarBadgeCarrito(result.data.total_items_carrito);
                })
                .catch(function (error) {
                    modalFeedback.textContent = error.message || 'Error al agregar al carrito.';
                    modalFeedback.style.color = '#dc3545';
                });
        });
    }
});
