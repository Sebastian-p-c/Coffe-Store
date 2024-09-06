from django.shortcuts import render

def index(request):
    context={}
    return render(request, 'menu/index.html', context)

def nosotros(request):
    context={}
    return render(request, 'menu/nosotros.html', context)