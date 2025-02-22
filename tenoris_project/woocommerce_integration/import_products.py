# import_products.py
import json
import os
import requests
from inventario.models import Producto, Variacion
from configuracion.models import Categoria, Color, TallaMujer, TallaNina, TallaCalzado, Metal, AlturaTacon
from proveedores.models import Proveedor
from django.contrib.auth.models import User

def parse_sku(sku):
    """
    Parsea el SKU para extraer el tipo de producto y el proveedor.
    """
    tipo_producto = sku[:2]
    proveedor = sku[2:4]
    correlativo = sku[4:]
    return tipo_producto, proveedor, correlativo

def import_products_from_json(filename="productos.json"):
    """
    Importa los productos desde un archivo JSON a la base de datos.
    """
    with open(filename, "r", encoding="utf-8") as file:
        products = json.load(file)

    for product_data in products:
        # Extraer información básica del producto
        sku = product_data["sku"]
        nombre = product_data["name"]
        descripcion = product_data["description"]
        categoria_nombre = product_data["categories"][0]["name"] if product_data["categories"] else "Sin categoría"
        tipo_operacion = "venta"  # Por defecto, asumimos que es venta

        # Parsear el SKU para obtener el proveedor
        tipo_producto, proveedor_codigo, _ = parse_sku(sku)

        # Crear o obtener el proveedor
        proveedor, _ = Proveedor.objects.get_or_create(codigo=proveedor_codigo)

        # Crear o obtener la categoría
        categoria, _ = Categoria.objects.get_or_create(nombre=categoria_nombre)

        # Crear el producto
        producto, created = Producto.objects.get_or_create(
            sku=sku,
            defaults={
                "nombre": nombre,
                "descripcion": descripcion,
                "categoria": categoria,
                "proveedor": proveedor,
                "tipo_operacion": tipo_operacion,
                "usuario": User.objects.first()  # Asignar un usuario por defecto
            }
        )

        # Procesar variaciones
        for variation in product_data.get("variations", []):
            variacion_data = requests.get(
                f"{os.getenv('WOOCOMMERCE_URL')}/wp-json/wc/v3/products/{product_data['id']}/variations/{variation}",
                auth=(os.getenv("WOOCOMMERCE_CONSUMER_KEY"), os.getenv("WOOCOMMERCE_CONSUMER_SECRET"))
            ).json()

            # Extraer atributos de la variación
            color_nombre = None
            talla_mujer_nombre = None

            if variacion_data.get("attributes"):
                for attribute in variacion_data["attributes"]:
                    if attribute["name"].lower() == "color":
                        color_nombre = attribute["option"]
                    elif attribute["name"].lower() == "talla":
                        talla_mujer_nombre = attribute["option"]

            # Crear o obtener los atributos
            color, _ = Color.objects.get_or_create(nombre=color_nombre) if color_nombre else (None, None)
            talla_mujer, _ = TallaMujer.objects.get_or_create(nombre=talla_mujer_nombre) if talla_mujer_nombre else (None, None)

            # Manejar stock_quantity
            stock = variacion_data.get("stock_quantity") or 0

            # Crear la variación
            Variacion.objects.create(
                producto=producto,
                sku=variacion_data["sku"],
                color=color,
                talla_mujer=talla_mujer,
                precio=variacion_data["price"],
                stock=stock,
                usuario=User.objects.first()  # Asignar un usuario por defecto
            )

    print("Importación completada.")