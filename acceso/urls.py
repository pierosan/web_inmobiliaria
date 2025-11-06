from django.urls import path
from . import views

app_name = "acceso"

urlpatterns = [
    path("registro/", views.vistaRegistro.as_view(), name="registro"),
    path("login/", views.vistaLogin.as_view(), name="login"),
    path("logout/", views.vistaLogout.as_view(), name="logout"),
]