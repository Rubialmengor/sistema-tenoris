from django.contrib import admin
from .models import MetodoPago

# Register your models here.
@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

