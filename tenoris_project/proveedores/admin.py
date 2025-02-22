from django.contrib import admin
from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'contacto')
    search_fields = ('codigo', 'nombre')