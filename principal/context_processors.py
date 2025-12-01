from .models import ConfiguracionWeb

def site_config(request):
    config = ConfiguracionWeb.objects.first()
    return {'config_web': config}
