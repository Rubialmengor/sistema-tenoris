from django.contrib import admin
from .models import Tallaje, FotoTallaje  # Importa ambos modelos

# Inline para Fotos de Tallaje
class FotoTallajeInline(admin.TabularInline):
    model = FotoTallaje
    extra = 1  # Número de formularios vacíos para agregar fotos

# Registro del modelo Tallaje
@admin.register(Tallaje)
class TallajeAdmin(admin.ModelAdmin):
    list_display = (
        'venta',
        'fecha_tallaje',
        'proximo_tallaje',
        'usuario'
    )
    list_filter = ('fecha_tallaje', 'proximo_tallaje')
    inlines = [FotoTallajeInline]  # Agregar fotos directamente

# Registro del modelo FotoTallaje
@admin.register(FotoTallaje)
class FotoTallajeAdmin(admin.ModelAdmin):
    list_display = ('tallaje', 'descripcion', 'fecha_creacion')
    search_fields = ('tallaje__id',)