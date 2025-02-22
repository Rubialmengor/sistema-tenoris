from django.db import models
from django.contrib.auth.models import User

# Modelo: Tallaje (Nuevo modelo para el registro de tallajes)
class Tallaje(models.Model):
    venta = models.ForeignKey('ventas.Venta', related_name='tallajes', on_delete=models.CASCADE)  # Usa una cadena para evitar dependencias circulares
    fecha_tallaje = models.DateField(blank=True, null=True)  # Fecha del tallaje
    proximo_tallaje = models.DateField(blank=True, null=True)  # Fecha del próximo tallaje
    foto = models.ImageField(upload_to='tallajes/', blank=True, null=True)  # Foto del tallaje
    comentarios = models.TextField(blank=True, null=True)  # Comentarios adicionales
    firma_cliente = models.ImageField(upload_to='firmas/', blank=True, null=True)  # Firma del cliente
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)  # Usuario que registra el tallaje

    def __str__(self):
        return f"Tallaje de Venta #{self.venta.id} - {self.fecha_tallaje}"

# Modelo: FotoTallaje
class FotoTallaje(models.Model):
    tallaje = models.ForeignKey(Tallaje, related_name='fotos', on_delete=models.CASCADE)  # Relación con Tallaje
    foto = models.ImageField(upload_to='tallajes/')  # Foto del tallaje
    descripcion = models.CharField(max_length=255, blank=True, null=True)  # Descripción opcional
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha automática de creación
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)  # Usuario que sube la foto

    def __str__(self):
        return f"Foto de Tallaje #{self.tallaje.id}"