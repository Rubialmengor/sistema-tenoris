from django.contrib import admin
from .models import TipoTalla, Color, TallaMujer, TallaNina, TallaCalzado, Metal, AlturaTacon, EstadoProducto, TipoOperacion

@admin.register(TipoTalla)
class TipoTallaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(TallaMujer)
class TallaMujerAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(TallaNina)
class TallaNinaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(TallaCalzado)
class TallaCalzadoAdmin(admin.ModelAdmin):
    list_display = ('medida_cm', 'tipo')
    search_fields = ('tipo',)


@admin.register(Metal)
class MetalAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(AlturaTacon)
class AlturaTaconAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(EstadoProducto)
class EstadoProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# Configuración de Tipo de Operación en el admin
@admin.register(TipoOperacion)
class TipoOperacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    search_fields = ('nombre', 'slug')