from django.urls import path
from . import views

app_name = "principal"

urlpatterns = [
    path("", views.vistaInicio.as_view(), name="inicio"),
    path("acerca/", views.vistaAcerca.as_view(), name="acerca"),
    path("contacto/", views.vistaContacto.as_view(), name="contacto"),
    path("lista-propiedades/", views.vistaListaPropiedades.as_view(), name="lista_propiedades"),
    path("propiedad/<int:pk>/", views.vistaDetallePropiedad.as_view(), name="propiedad_detalle"),
    
    # Rutas de Administración
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/crear/", views.crear_propiedad, name="crear_propiedad"),
    path("dashboard/editar/<int:pk>/", views.editar_propiedad, name="editar_propiedad"),
    path("dashboard/eliminar/<int:pk>/", views.eliminar_propiedad, name="eliminar_propiedad"),
]
