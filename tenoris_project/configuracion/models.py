from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    padre = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    tipo_talla = models.ForeignKey('TipoTalla', on_delete=models.SET_NULL, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class TipoTalla(models.Model):
    nombre = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Color(models.Model):
    nombre = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class TallaMujer(models.Model):
    nombre = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class TallaNina(models.Model):
    nombre = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class TallaCalzado(models.Model):
    medida_cm = models.DecimalField(max_digits=5, decimal_places=2)
    tipo = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.medida_cm} cm ({self.tipo})"

class Metal(models.Model):
    nombre = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class AlturaTacon(models.Model):
    nombre = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class EstadoProducto(models.Model):
    nombre = models.CharField(max_length=50, unique=True)  # Ejemplo: "Pendiente", "En Proceso", "Entregado"
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
# configuracion/models.py
class TipoOperacion(models.Model):
    nombre = models.CharField(max_length=20, unique=True)  # Venta, Renta, Ambos
    slug = models.SlugField(unique=True)  # Slug compatible con WooCommerce ('renta-o-venta')

    def __str__(self):
        return self.nombre
