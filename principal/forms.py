from django import forms
from .models import Propiedad, ImagenPropiedad
from django.contrib.auth import get_user_model # To get the User model
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class AgenteForm(UserCreationForm):
    # Campos extra del perfil de agente
    foto = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    telefono = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True # Mark as staff/agent
        if commit:
            user.save()
            # Guardar datos del perfil
            if hasattr(user, 'perfil_agente'):
                perfil = user.perfil_agente
                perfil.telefono = self.cleaned_data['telefono']
                if self.cleaned_data['foto']:
                    perfil.foto = self.cleaned_data['foto']
                perfil.save()
        return user

class AgenteEditForm(forms.ModelForm):
    # Campos extra del perfil de agente
    foto = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    telefono = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-popular campos del perfil si existen
        if self.instance.pk and hasattr(self.instance, 'perfil_agente'):
            self.fields['telefono'].initial = self.instance.perfil_agente.telefono
            # Foto no se puede prepopular con valor, pero se maneja en visualización

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Guardar perfil
            if hasattr(user, 'perfil_agente'):
                perfil = user.perfil_agente
                perfil.telefono = self.cleaned_data['telefono']
                if self.cleaned_data['foto']:
                    perfil.foto = self.cleaned_data['foto']
                perfil.save()
        return user

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
