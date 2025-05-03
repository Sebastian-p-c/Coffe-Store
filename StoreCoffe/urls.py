from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UsuarioViewSet, registrar_usuario, login_view, UsuarioView,  CambiarContrasenaView, EliminarCuentaView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet) 

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'), 
    path('detalleproducto/', views.detalleproducto, name='detalleproducto'),
    path("logout/", views.logout_view, name="logout"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh
    path('api/registro/', views.registrar_usuario, name='registro_api'),
    path('api/usuarios/me/', UsuarioView.as_view(), name='usuario-me'),
    path('api/', include(router.urls)),
    path('api/usuarios/cambiar-password/', CambiarContrasenaView.as_view(), name='cambiar_password'),

    # Eliminar cuenta por correo electrónico
    path('api/usuarios/eliminar_cuenta/', EliminarCuentaView.as_view(), name='eliminar_cuenta'),
]