from django import forms
from .models import Propiedad, ImagenPropiedad
from django.contrib.auth import get_user_model # To get the User model
from django.forms import inlineformset_factory

User = get_user_model()

class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la propiedad'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción detallada'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'antes_precio_etiqueta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: "desde", "al mes"'}),
            'despues_precio_etiqueta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: "por mes", "negociable"'}),
            'area_m2': forms.NumberInput(attrs={'class': 'form-control'}),
            'dormitorios': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'banos': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'latitud': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control'}),
            'ubicacion_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://maps.google.com/...'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
            'distrito': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Lima, Ica'}),
            'video': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL de video de YouTube'}),
            'planos_imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'estado_propiedad': forms.Select(attrs={'class': 'form-control'}),
            'agente_inmobiliario': forms.Select(attrs={'class': 'form-control'}), # Will display a dropdown of User objects
        }

# Form for individual images
class ImagenPropiedadForm(forms.ModelForm):
    class Meta:
        model = ImagenPropiedad
        fields = ['imagen'] # Only the image field
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }

# Formset for multiple images related to a property
PropiedadImagenFormSet = inlineformset_factory(
    Propiedad, 
    ImagenPropiedad, 
    form=ImagenPropiedadForm, 
    extra=1, # Show 1 empty form by default
    can_delete=True
)
