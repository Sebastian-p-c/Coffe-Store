from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm, AutheticationForms
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import usuario


def index(request):
    context={}
    return render(request, 'menu/index.html', context)

def nosotros(request):
    context={}
    return render(request, 'menu/nosotros.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        clave = request.POST["clave"]

        try:
            user = usuario.objects.get(username=username, clave=clave)  # Verifica si el usuario existe con la clave
            # Si el usuario es encontrado, puedes iniciar sesión usando Django's session framework
            # Aquí podrías querer hacer tu lógica para iniciar sesión o redirigir
            return redirect("index")  # Redirige al usuario a la página de inicio
        except usuario.DoesNotExist:
            messages.error(request, "Nombre de usuario o contraseña incorrectos")
    return render(request, "menu/login.html")

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = RegistroUsuarioForm()
    return render(request, 'menu/registro.html', {'form': form})

def detalleproducto(request):
    context={}
    return render(request, 'menu/detalle-producto.html', context)

def logout_view(request):
    logout(request)
    return redirect("login")
