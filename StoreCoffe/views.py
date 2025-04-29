from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm, AutheticationForms
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import usuario, Transaccion
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import TransaccionSerializer


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

class TransaccionViewSet(viewsets.ModelViewSet):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer
    lookup_field = 'token'  # Usamos token como ID en la URL

    def create(self, request):
        serializer = TransaccionSerializer(data=request.data)
        if serializer.is_valid():
            transaccion = serializer.save()
            return Response({'token': transaccion.token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def estado(self, request, token=None):
        transaccion = self.get_object()
        return Response({'estado': transaccion.estado})

    @action(detail=True, methods=['put'])
    def confirmar(self, request, token=None):
        transaccion = self.get_object()
        transaccion.estado = 'aprobada'
        transaccion.save()
        return Response({'mensaje': 'Transacción confirmada'})   
