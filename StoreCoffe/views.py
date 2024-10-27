from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm
from .models import usuario

def index(request):
    context={}
    return render(request, 'menu/index.html', context)

def nosotros(request):
    context={}
    return render(request, 'menu/nosotros.html', context)

def login(request):
    context={}
    return render(request, 'menu/login.html', context)

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # Guardar el usuario en la base de datos
            form.save()
            return redirect('login')  # Redirige al login una vez registrado
    else:
        form = RegistroUsuarioForm()
    return render(request, 'menu/registro.html', {'form': form})

def detalleproducto(request):
    context={}
    return render(request, 'menu/detalle-producto.html', context)
