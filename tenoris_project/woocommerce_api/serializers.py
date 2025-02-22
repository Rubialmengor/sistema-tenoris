# woocommerce_api/serializers.py
from rest_framework import serializers

class ProductoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    sku = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    categories = serializers.ListField(child=serializers.DictField())

class VariacionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    attributes = serializers.ListField(child=serializers.DictField())
    price = serializers.DecimalField(max_digits=10, decimal_places=2)