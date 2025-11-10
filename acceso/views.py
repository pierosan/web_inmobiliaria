from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout

# Create your views here.

class vistaRegistro(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "registro.html", {'form': form})
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada exitosamente. ¡Ahora puedes iniciar sesión!")
            return redirect('login')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")

class vistaLogin(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)
            return redirect('principal:inicio') 
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

class vistaLogout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Has cerrado sesión correctamente.")
        return redirect('principal:inicio') 