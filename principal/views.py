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

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Filtering
        tipo = self.request.GET.get('tipo')
        categoria = self.request.GET.get('categoria')
        departamento = self.request.GET.get('departamento')
        distrito = self.request.GET.get('distrito')
        
        if tipo:
            qs = qs.filter(tipo=tipo)
        if categoria:
            qs = qs.filter(categoria=categoria)
        if departamento:
            qs = qs.filter(departamento=departamento)
        if distrito:
            qs = qs.filter(distrito=distrito)
            
        # Ordering
        orden = self.request.GET.get('orden')
        if orden == 'precio_asc':
            qs = qs.order_by('precio')
        elif orden == 'precio_desc':
            qs = qs.order_by('-precio')
        elif orden == 'antiguo':
            qs = qs.order_by('creado_en')
        else:
            # Default: Recientes primero
            qs = qs.order_by('-creado_en')
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pass distinct values for dropdowns
        # Note: In a real large-scale app, you might cache these or optimize query
        context['distritos'] = Propiedad.objects.values_list('distrito', flat=True).distinct().order_by('distrito')
        context['departamentos'] = Propiedad.objects.values_list('departamento', flat=True).distinct().order_by('departamento')
        
        # Pass choices from model (generic View doesn't pass them automatically)
        context['tipos_choices'] = Propiedad.TIPO_OFERTA_CHOICES
        context['categorias_choices'] = Propiedad.CATEGORIA_CHOICES
        
        return context

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