# paginas/models.py
from django.db import models

class Propiedad(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=255)
    descripcion = models.TextField()
    
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio de la propiedad")
    dormitorios = models.PositiveIntegerField(default=0)
    banos = models.PositiveIntegerField(default=0, verbose_name="baños")
    garaje = models.PositiveIntegerField(default=0, help_text="Capacidad del garaje (en autos)")
    area = models.PositiveIntegerField(default=0, help_text="Área en metros cuadrados (m²)")
    anio = models.PositiveIntegerField(verbose_name="año de construcción", null=True, blank=True)

    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=10, decimal_places=6)

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