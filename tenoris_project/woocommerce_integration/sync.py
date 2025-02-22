# woocommerce_integration/sync.py
from inventario.models import Producto, Categoria
from woocommerce_integration.utils import get_wcapi

def obtener_productos():
    """Obtiene todos los productos desde WooCommerce."""
    wcapi = get_wcapi()
    productos = []
    page = 1
    while True:
        response = wcapi.get("products", params={"per_page": 100, "page": page})
        if response.status_code != 200:
            print(f"Error al obtener productos: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        productos.extend(data)
        page += 1

    return productos


def guardar_productos_locales(productos):
    """Guarda los productos obtenidos de WooCommerce en la base de datos local."""
    for producto in productos:
        # Obtener o crear la categoría principal
        categoria_id = producto["categories"][0]["id"] if producto["categories"] else None
        categoria = Categoria.objects.get_or_create(
            woocommerce_id=categoria_id,
            defaults={"nombre": producto["categories"][0]["name"] if producto["categories"] else "Sin Categoría"}
        )[0]

        # Crear o actualizar el producto
        Producto.objects.update_or_create(
            woocommerce_id=producto["id"],
            defaults={
                "sku": producto["sku"],
                "nombre": producto["name"],
                "descripcion": producto["description"],
                "precio": producto["price"],
                "categoria": categoria,
            }
        )