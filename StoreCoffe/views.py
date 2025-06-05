from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Usuario
from .serializers import UsuarioSerializer
from .forms import RegistroUsuarioForm

# -------------------------
# Vistas HTML
# -------------------------
def index(request):
    return render(request, 'menu/index.html')

def nosotros(request):
    return render(request, 'menu/nosotros.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["clave"]
        user = authenticate(request, username=username, password=password)
        if user:
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
    return render(request, 'menu/detalle-producto.html')

def cafedivino(request):
    return render(request, 'menu/cafedivino.html')

def cafeelite(request):
    return render(request, 'menu/cafeelite.html')

def cafegolden(request):
    return render(request, 'menu/cafegolden.html')

def cafehacking(request):
    return render(request, 'menu/cafehacking.html')

def cafepower(request):
    return render(request, 'menu/cafepower.html')

def cafepremium(request):
    return render(request, 'menu/cafepremium.html')

def cafeultimate(request):
    return render(request, 'menu/cafeultimate.html')

def cafeultimateplatino(request):
    return render(request, 'menu/cafeultimateplatino.html')

def cafeultimatepremium(request):
    return render(request, 'menu/cafeultimatepremium.html')

def logout_view(request):
    logout(request)
    return redirect("login")

# -------------------------
# API REST
# -------------------------

# Registrar usuario por API
@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_usuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtener datos del usuario autenticado
class UsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

# Cambiar contraseña por usuario autenticado
class CambiarContrasenaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nueva_clave = request.data.get('nueva_clave')
        if not nueva_clave:
            return Response({'error': 'Debe proporcionar una nueva contraseña'}, status=400)
        user = request.user
        user.set_password(nueva_clave)
        user.save()
        return Response({'mensaje': 'Contraseña actualizada correctamente'})
    
# Eliminar cuenta del usuario autenticado
class EliminarCuentaView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'mensaje': 'Cuenta eliminada correctamente'}, status=204)

# ViewSet para admin/API
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def mi_usuario(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
