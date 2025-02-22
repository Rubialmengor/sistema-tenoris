from django.db import models
from django.contrib.auth.models import User
from configuracion.models import Categoria
from proveedores.models import Proveedor

# Modelo: Producto
class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )  # Precio de venta
    precio_renta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )  # Precio de renta
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    tipo_operacion = models.CharField(
        max_length=10,
        choices=[
            ('venta', 'Venta'),
            ('renta', 'Renta'),
            ('ambos', 'Venta y Renta')
        ],
        default='venta'
    )  # Tipo de operación permitida
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
        
# Modelo: Stock
class Stock(models.Model):
    OPCIONES_DISPONIBILIDAD = [
        ('stock', 'Disponible en Stock'),
        ('cliente', 'Reservado para Cliente'),
    ]

    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    color = models.ForeignKey('configuracion.Color', on_delete=models.CASCADE)
    talla_mujer = models.ForeignKey('configuracion.TallaMujer', on_delete=models.SET_NULL, blank=True, null=True)
    talla_nina = models.ForeignKey('configuracion.TallaNina', on_delete=models.SET_NULL, blank=True, null=True)
    talla_calzado = models.ForeignKey('configuracion.TallaCalzado', on_delete=models.SET_NULL, blank=True, null=True)
    metal = models.ForeignKey('configuracion.Metal', on_delete=models.SET_NULL, blank=True, null=True)
    altura_tacon = models.ForeignKey('configuracion.AlturaTacon', on_delete=models.SET_NULL, blank=True, null=True)
    codigo_barra = models.CharField(max_length=50, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField()
    ubicacion = models.ForeignKey('Ubicacion', on_delete=models.SET_NULL, blank=True, null=True)
    disponibilidad = models.CharField(
        max_length=10,
        choices=OPCIONES_DISPONIBILIDAD,
        default='stock'
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producto.nombre} - {self.color.nombre}"
    
# Modelo: ImagenProducto (Nuevo modelo para múltiples imágenes)
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/')
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
        
# Modelo: Ubicación
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# inventario/models.py
class Variacion(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    sku = models.CharField(max_length=50, unique=True)
    color = models.ForeignKey('configuracion.Color', on_delete=models.SET_NULL, blank=True, null=True)
    talla_mujer = models.ForeignKey('configuracion.TallaMujer', on_delete=models.SET_NULL, blank=True, null=True)
    talla_nina = models.ForeignKey('configuracion.TallaNina', on_delete=models.SET_NULL, blank=True, null=True)
    talla_calzado = models.ForeignKey('configuracion.TallaCalzado', on_delete=models.SET_NULL, blank=True, null=True)
    metal = models.ForeignKey('configuracion.Metal', on_delete=models.SET_NULL, blank=True, null=True)
    altura_tacon = models.ForeignKey('configuracion.AlturaTacon', on_delete=models.SET_NULL, blank=True, null=True)
    tipo_operacion = models.ForeignKey('configuracion.TipoOperacion', on_delete=models.SET_NULL, blank=True, null=True)  # Nuevo campo
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        talla = self.talla_mujer or self.talla_nina or self.talla_calzado
        if self.talla_calzado:
            talla = f"Talla Calzado: {self.talla_calzado.medida_cm} cm ({self.talla_calzado.tipo})"

        color = self.color.nombre if self.color else "Sin color"
        metal = f" - Metal: {self.metal.nombre}" if self.metal else ""
        altura_tacon = f" - Altura Tacón: {self.altura_tacon.nombre}" if self.altura_tacon else ""
        tipo_op = f" - {self.tipo_operacion.nombre}" if self.tipo_operacion else ""

        return f"{self.producto.nombre} - Color: {color} - {talla}{metal}{altura_tacon}{tipo_op}"
