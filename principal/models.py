from django.db import models
from django.conf import settings # Import settings for AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver
import re

class Agente(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil_agente')
    foto = models.ImageField(upload_to='agentes/', blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True, help_text="Breve descripción para la sección 'Sobre mí'")

    def get_whatsapp_number(self):
        if not self.telefono:
            return ""
        return ''.join(filter(str.isdigit, self.telefono))

    def __str__(self):
        return f"Perfil de Agente: {self.usuario.username}"

# Señales para crear/actualizar automáticamente el perfil de Agente
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil_agente(sender, instance, created, **kwargs):
    if created:
        # Crear perfil solo si es staff o si queremos que todos tengan perfil
        # Por ahora creamos para todos para evitar errores, o filtramos por is_staff
        Agente.objects.create(usuario=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def guardar_perfil_agente(sender, instance, **kwargs):
    # Guardar el perfil si existe, sino crearlo (safe guard)
    if hasattr(instance, 'perfil_agente'):
        instance.perfil_agente.save()
    else:
        Agente.objects.create(usuario=instance)

class ConfiguracionWeb(models.Model):
    """
    Modelo Singleton para guardar la configuración global del sitio.
    Solo debería existir una fila en esta tabla.
    """
    agente_principal = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='configuracion_principal',
        limit_choices_to={'is_staff': True},
        help_text="Este agente será el contacto principal que aparecerá en el pie de página, contacto, etc."
    )
    
    def __str__(self):
        return "Configuración del Sitio Web"

    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionWeb.objects.exists():
            # Si ya existe uno, actualizamos el primero en lugar de crear uno nuevo
            # O lanzamos error. Para simplicidad, forzamos a que sea el ID 1 si queremos singleton estricto
            # Pero aquí simplemente permitimos guardar y usaremos .first() en el view
            pass
        return super(ConfiguracionWeb, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Configuración Web"
        verbose_name_plural = "Configuración Web"

class Propiedad(models.Model):
    # Detalles básicos
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    # Precio y etiquetas
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio de la propiedad")
    antes_precio_etiqueta = models.CharField(max_length=50, blank=True, null=True, 
                                            help_text="Ej: 'desde', 'al mes'")
    despues_precio_etiqueta = models.CharField(max_length=50, blank=True, null=True, 
                                             help_text="Ej: 'por mes', 'negociable'")
    
    # Características
    area_m2 = models.DecimalField(max_digits=7, decimal_places=2, help_text="Área en metros cuadrados")
    dormitorios = models.PositiveIntegerField(default=0, help_text="Número de dormitorios")
    banos = models.PositiveIntegerField(default=0, help_text="Número de baños")
    
    # Ubicación
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    ubicacion_url = models.URLField(max_length=500, null=True, blank=True, 
                                    help_text="URL de Google Maps o similar")
    direccion = models.CharField(max_length=255, help_text="Dirección completa de la propiedad")
    distrito = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100, help_text="Ej: Lima, Ica", default="Lima")

    # Multimedia
    video = models.URLField(max_length=255, null=True, blank=True, help_text="URL de video de YouTube")
    planos_imagen = models.ImageField(upload_to='planos/', blank=True, null=True, 
                                     help_text="Imagen de los planos de la propiedad")
    
    # Categorización
    CATEGORIA_CHOICES = [
        ('CASA', 'Casa'),
        ('DEPARTAMENTO', 'Departamento'),
        ('TERRENO', 'Terreno'),
        ('OFICINA', 'Oficina'),
        ('LOCAL_COMERCIAL', 'Local Comercial'),
        ('OTROS', 'Otros'),
    ]
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='CASA')

    TIPO_OFERTA_CHOICES = [
        ('ALQUILER', 'Alquiler'),
        ('ALQUILER_VENTA', 'Alquiler y Venta'),
        ('VENTA', 'Venta'),
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_OFERTA_CHOICES, default='VENTA')

    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('NO_DISPONIBLE', 'No disponible'),
        ('NUEVO', 'Nuevo'),
        ('VENDIDO', 'Vendido'),
        ('ALQUILADO', 'Alquilado'),
    ]
    estado_propiedad = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='DISPONIBLE')

    # Agente Inmobiliario
    agente_inmobiliario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='propiedades_gestionadas',
        help_text="Agente responsable de la propiedad"
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"
        ordering = ['-creado_en']

    def __str__(self):
        return self.nombre

    def get_video_embed_url(self):
        if not self.video:
            return None
        
        # Regex for YouTube URLs
        # Supports:
        # - https://www.youtube.com/watch?v=VIDEO_ID
        # - https://youtu.be/VIDEO_ID
        # - https://www.youtube.com/embed/VIDEO_ID
        regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        
        match = re.search(regex, self.video)
        
        if match:
            video_id = match.group(1)
            return f'https://www.youtube-nocookie.com/embed/{video_id}'
        
        return self.video

class ImagenPropiedad(models.Model):
    propiedad = models.ForeignKey(
        Propiedad, 
        on_delete=models.CASCADE, 
        related_name="imagenes"
    )
    imagen = models.ImageField(upload_to='propiedades/', verbose_name="Imagen", null=True, blank=True)

    class Meta:
        verbose_name = "Imagen de Propiedad"
        verbose_name_plural = "Imágenes de Propiedades"

    def __str__(self):
        return f"Imagen para {self.propiedad.nombre}"
