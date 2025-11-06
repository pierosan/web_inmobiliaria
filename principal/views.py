from django.views import generic
from .models import Propiedad

class vistaInicio(generic.ListView):
    model = Propiedad
    template_name = "index.html"

class vistaAcerca(generic.TemplateView):
    template_name = "acerca.html"

class vistaContacto(generic.TemplateView):
    template_name = "contacto.html"

class vistaListaPropiedades(generic.TemplateView):
    template_name = "lista_propiedades.html"

class vistaDetallePropiedad(generic.DetailView):
    model = Propiedad
    template_name = "detalle_propiedad.html"
