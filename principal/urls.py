from django.urls import path
from . import views

app_name = "principal"

urlpatterns = [
    path("", views.vistaInicio.as_view(), name="inicio"),
    path("acerca/", views.vistaAcerca.as_view(), name="acerca"),
    path("contacto/", views.vistaContacto.as_view(), name="contacto"),
    path("buscar/", views.vistaBusquedaPropiedades.as_view(), name="buscar_propiedades"),
    path("lista-propiedades/", views.vistaListaPropiedades.as_view(), name="lista_propiedades"),
    path("propiedad/<int:pk>/", views.vistaDetallePropiedad.as_view(), name="propiedad_detalle"),
    
    # Rutas de Administración
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/crear/", views.crear_propiedad, name="crear_propiedad"),
    path("dashboard/editar/<int:pk>/", views.editar_propiedad, name="editar_propiedad"),
    path("dashboard/eliminar/<int:pk>/", views.eliminar_propiedad, name="eliminar_propiedad"),

    # Rutas de Gestión de Agentes
    path("dashboard/agentes/crear/", views.crear_agente, name="crear_agente"),
    path("dashboard/agentes/editar/<int:pk>/", views.editar_agente, name="editar_agente"),
    path("dashboard/agentes/eliminar/<int:pk>/", views.eliminar_agente, name="eliminar_agente"),
]
