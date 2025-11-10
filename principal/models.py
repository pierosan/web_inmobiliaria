# paginas/models.py
from django.db import models

class Propiedad(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio de la propiedad")
    area_m2 = models.DecimalField(max_digits=7, decimal_places=2, help_text="Área en metros cuadrados")

    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=10, decimal_places=6)
    ubicacion_url = models.URLField(max_length=500, null=True, blank=True)

    direccion = models.CharField(max_length=255)
    distrito = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)

    video = models.URLField(max_length=255, null=True, blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"
        ordering = ['-creado_en']

    def __str__(self):
        return self.nombre

class ImagenPropiedad(models.Model):
    propiedad = models.ForeignKey(
        Propiedad, 
        on_delete=models.CASCADE, 
        related_name="imagenes"
    )
    imagen_url = models.URLField(max_length=500, verbose_name="URL de la Imagen")

    class Meta:
        verbose_name = "Imagen de Propiedad"
        verbose_name_plural = "Imágenes de Propiedades"

    def __str__(self):
        return f"Imagen para {self.propiedad.nombre}"