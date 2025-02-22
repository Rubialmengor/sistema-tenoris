from django.contrib import admin
from .models import Venta, DetalleVenta, Abono, Factura

# Inline para Facturas
class FacturaInline(admin.TabularInline):
    model = Factura
    extra = 1

# Inline para Abonos
class AbonoInline(admin.TabularInline):
    model = Abono
    extra = 1

# Inline para DetalleVenta
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    readonly_fields = ('precio_unitario', 'subtotal')

@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
    list_display = ('venta', 'monto', 'fecha_abono', 'comentarios')
    list_filter = ('fecha_abono', 'venta__id')
    readonly_fields = ('fecha_abono',)

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = (
        'producto',
        'venta',
        'cantidad',
        'precio_unitario',
        'subtotal',
        'tipo_operacion',
        'comentarios',
        'usuario'
    )
    list_filter = ('tipo_operacion', 'venta__id')
    search_fields = ('producto__nombre', 'venta__id')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'fecha_pedido',
        'fecha_compromiso',
        'fecha_evento',
        'estado',
        'total',
        'anticipo',
        'saldo_pendiente',
        'metodo_pago'
    )
    search_fields = ('id', 'cliente__nombre')
    list_filter = ('estado__nombre', 'fecha_pedido', 'fecha_compromiso', 'fecha_evento')
    readonly_fields = ('fecha_pedido', 'saldo_pendiente')
    inlines = [DetalleVentaInline, AbonoInline, FacturaInline]  # Elimina TallajeInline

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'venta', 'fecha_emision', 'monto')
    list_filter = ('fecha_emision', 'venta__id')
    search_fields = ('numero_factura', 'venta__id')