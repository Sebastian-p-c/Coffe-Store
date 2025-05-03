# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from .forms import RegistroUsuarioForm
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Usuario
from .serializers import UsuarioSerializer
from .forms import RegistroUsuarioForm

def index(request):
    context = {}
    return render(request, 'menu/index.html', context)

def nosotros(request):
    context = {}
    return render(request, 'menu/nosotros.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["clave"]
        
        # Usar el sistema de autenticación de Django
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
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
    context = {}
    return render(request, 'menu/detalle-producto.html', context)

def logout_view(request):
    logout(request)
    return redirect("login")

# Vista API REST para registrar usuario
@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_usuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ViewSet para la gestión completa de usuarios
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
    
    # Opcional: Puedes personalizar los métodos para adaptarlos a tus necesidades
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # Método adicional: Obtener la información del usuario autenticado
    @action(detail=False, methods=['get'])
    def mi_usuario(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
