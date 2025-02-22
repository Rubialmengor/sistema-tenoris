from django.contrib import admin
from django.utils.html import format_html
from .models import Producto, Stock, ImagenProducto, Ubicacion, Variacion

# Clase personalizada para mostrar imágenes en el panel de administración
class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1  # Número de campos adicionales para agregar nuevas imágenes
    readonly_fields = ('imagen_preview',)

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="100" height="100" />', obj.imagen.url)
        return "(Sin imagen)"
    imagen_preview.short_description = 'Vista previa'

# Clase personalizada para el modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'precio_venta', 'precio_renta', 'categoria', 'proveedor', 'activo', 'tipo_operacion')
    list_filter = ('categoria', 'proveedor', 'activo', 'tipo_operacion')
    search_fields = ('sku', 'nombre')
    inlines = [ImagenProductoInline]  # Mostrar imágenes relacionadas con el producto

# Clase personalizada para el modelo Stock (variaciones)
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('producto_nombre', 'color', 'talla_mujer', 'talla_nina', 'stock', 'disponibilidad')
    list_filter = ('disponibilidad', 'color', 'talla_mujer', 'talla_nina')
    search_fields = ('producto__nombre', 'codigo_barra')

    def producto_nombre(self, obj):
        return obj.producto.nombre
    producto_nombre.short_description = 'Producto'

# Clase personalizada para el modelo ImagenProducto
@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'imagen_preview', 'descripcion')
    readonly_fields = ('imagen_preview',)

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="100" height="100" />', obj.imagen.url)
        return "(Sin imagen)"
    imagen_preview.short_description = 'Vista previa'

# Clase personalizada para el modelo Ubicación
@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# Clase personalizada para el modelo Variación
# Configuración de Variaciones en el admin con el nuevo campo 'tipo_operacion'
@admin.register(Variacion)
class VariacionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'sku', 'color', 'talla_mujer', 'talla_nina', 'talla_calzado', 'metal', 'altura_tacon', 'tipo_operacion', 'precio', 'stock', 'activo')
    search_fields = ('sku', 'producto__nombre')
    list_filter = ('color', 'tipo_operacion', 'activo')