from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Propiedad
from .forms import PropiedadForm, PropiedadImagenFormSet # Import PropiedadImagenFormSet

# --- Vistas Públicas ---

class vistaInicio(generic.ListView):
    model = Propiedad
    template_name = "index.html"

class vistaAcerca(generic.TemplateView):
    template_name = "acerca.html"

class vistaContacto(generic.TemplateView):
    template_name = "contacto.html"

class vistaListaPropiedades(generic.ListView):
    model = Propiedad
    template_name = "lista_propiedades.html"

class vistaDetallePropiedad(generic.DetailView):
    model = Propiedad
    template_name = "detalle_propiedad.html"

# --- Vistas de Administración ---

def es_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(es_admin)
def admin_dashboard(request):
    propiedades = Propiedad.objects.all().order_by('-creado_en')
    return render(request, 'admin_dashboard.html', {'propiedades': propiedades})

@login_required
@user_passes_test(es_admin)
def crear_propiedad(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        formset = PropiedadImagenFormSet(request.POST, request.FILES, prefix='imagenes')
        if form.is_valid() and formset.is_valid():
            propiedad = form.save()
            formset.instance = propiedad
            formset.save()
            messages.success(request, 'Propiedad creada exitosamente.')
            return redirect('principal:admin_dashboard')
    else:
        form = PropiedadForm()
        formset = PropiedadImagenFormSet(prefix='imagenes')
    return render(request, 'propiedad_form.html', {'form': form, 'formset': formset, 'titulo': 'Crear Propiedad'})

@login_required
@user_passes_test(es_admin)
def editar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES, instance=propiedad)
        formset = PropiedadImagenFormSet(request.POST, request.FILES, instance=propiedad, prefix='imagenes')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Propiedad actualizada exitosamente.')
            return redirect('principal:admin_dashboard')
    else:
        form = PropiedadForm(instance=propiedad)
        formset = PropiedadImagenFormSet(instance=propiedad, prefix='imagenes')
    return render(request, 'propiedad_form.html', {'form': form, 'formset': formset, 'titulo': 'Editar Propiedad'})

@login_required
@user_passes_test(es_admin)
def eliminar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        propiedad.delete()
        messages.success(request, 'Propiedad eliminada correctamente.')
        return redirect('principal:admin_dashboard')
    return render(request, 'confirmar_eliminar.html', {'propiedad': propiedad})