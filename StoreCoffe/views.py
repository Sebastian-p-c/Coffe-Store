from django.shortcuts import render

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
    context={}
    return render(request, 'menu/registro.html', context)

def detalleproducto(request):
    context={}
    return render(request, 'menu/detalle-producto.html', context)