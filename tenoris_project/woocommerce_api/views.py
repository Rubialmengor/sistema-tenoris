from django.shortcuts import render

# Create your views here.
# woocommerce_api/views.py
# woocommerce_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from woocommerce_integration.utils import get_wcapi  # Importación absoluta
from .serializers import ProductoSerializer, VariacionSerializer

class ObtenerProductosView(APIView):
    def get(self, request):
        wcapi = get_wcapi()
        response = wcapi.get("products")
        if response.status_code == 200:
            productos = response.json()
            serializer = ProductoSerializer(productos, many=True)
            return Response(serializer.data)
        return Response({"error": "No se pudieron obtener los productos"}, status=response.status_code)

class ObtenerVariacionesView(APIView):
    def get(self, request, product_id):
        wcapi = get_wcapi()
        response = wcapi.get(f"products/{product_id}/variations")
        if response.status_code == 200:
            variaciones = response.json()
            serializer = VariacionSerializer(variaciones, many=True)
            return Response(serializer.data)
        return Response({"error": "No se pudieron obtener las variaciones"}, status=response.status_code)