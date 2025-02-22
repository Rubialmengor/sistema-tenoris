# woocommerce_api/urls.py
from django.urls import path
from .views import ObtenerProductosView, ObtenerVariacionesView

urlpatterns = [
    path('productos/', ObtenerProductosView.as_view(), name='obtener_productos'),
    path('productos/<int:product_id>/variaciones/', ObtenerVariacionesView.as_view(), name='obtener_variaciones'),
]