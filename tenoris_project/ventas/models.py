from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from inventario.models import Producto, Stock
from django.core.validators import FileExtensionValidator
from contabilidad.models import MetodoPago


class Estado(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_compromiso = models.DateField(blank=True, null=True)
    fecha_evento = models.DateField(blank=True, null=True)
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, blank=True, null=True)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    anticipo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Calcular el total sumando los subtotales de los detalles de venta
        self.total = sum(detalle.subtotal for detalle in self.detalles.all())
        # Calcular el saldo pendiente restando el anticipo del total
        self.saldo_pendiente = self.total - self.anticipo
        # Si el estado es "Completado", el saldo pendiente se establece en 0
        if self.estado and self.estado.nombre.lower() == "completado":
            self.saldo_pendiente = 0
        # Guardar la venta
        super().save(*args, **kwargs)

    def actualizar_saldo_pendiente(self):
        # Actualizar el saldo pendiente sumando todos los abonos
        total_abonos = sum(abono.monto for abono in self.abonos.all())
        self.anticipo = total_abonos
        self.saldo_pendiente = self.total - self.anticipo
        self.save()

    def total_facturas(self):
        # Calcular el total de todas las facturas asociadas a la venta
        return sum(factura.monto for factura in self.facturas.all())

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre}"

class EstadoProducto(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variante = models.ForeignKey(Stock, on_delete=models.SET_NULL, blank=True, null=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        editable=False
    )
    descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_operacion = models.CharField(
        max_length=10,
        choices=[('venta', 'Venta'), ('renta', 'Renta')],
        default='venta'
    )
    comentarios = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    estado = models.ForeignKey(
        EstadoProducto,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None
    )

    def save(self, *args, **kwargs):
        # Asignar el precio unitario automáticamente desde el producto
        if not self.precio_unitario and self.producto:
            self.precio_unitario = self.producto.precio
        # Calcular el subtotal automáticamente
        self.subtotal = self.cantidad * self.precio_unitario
        if self.descuento:
            self.subtotal -= self.descuento
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Venta #{self.venta.id}"

class Abono(models.Model):
    venta = models.ForeignKey(Venta, related_name='abonos', on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_abono = models.DateTimeField(auto_now_add=True)
    constancia_pago = models.FileField(
        upload_to='abonos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])]
    )
    comentarios = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.venta.actualizar_saldo_pendiente()

    def __str__(self):
        return f"Abono de {self.monto} en Venta #{self.venta.id}"

class Factura(models.Model):
    numero_factura = models.CharField(max_length=50, unique=True)
    venta = models.ForeignKey(Venta, related_name='facturas', on_delete=models.SET_NULL, blank=True, null=True)
    fecha_emision = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    archivo_pdf = models.FileField(upload_to='facturas/')
    comentarios = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Factura #{self.numero_factura} - {self.fecha_emision}"