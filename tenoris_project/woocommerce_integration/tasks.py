# woocommerce_integration/tasks.py
from celery import shared_task
from .sync import obtener_productos, guardar_productos_locales

@shared_task
def sincronizar_productos():
    productos = obtener_productos()
    guardar_productos_locales(productos)