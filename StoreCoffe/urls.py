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
    path("cafedivino/", views.cafedivino, name="cafedivino"),
    path("cafeelite/", views.cafeelite, name="cafeelite"),
    path("cafegolden/", views.cafegolden, name="cafegolden"),
    path("cafehacking/", views.cafehacking, name="cafehacking"),
    path("cafepower/", views.cafepower, name="cafepower"),
    path("cafepremium/", views.cafepremium, name="cafepremium"),
    path("cafeultimate/", views.cafeultimate, name="cafeultimate"),
    path("cafeultimateplatino/", views.cafeultimateplatino, name="cafeultimateplatino"),
    path("cafeultimatepremium/", views.cafeultimatepremium, name="cafeultimatepremium"),
    path("logout/", views.logout_view, name="logout"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh
    path('api/registro/', views.registrar_usuario, name='registro_api'),
    path('api/usuarios/me/', UsuarioView.as_view(), name='usuario-me'),
    path('api/', include(router.urls)),
    path('api/usuarios/me/cambiar_contrasena/', CambiarContrasenaView.as_view(), name='cambiar_password'),

    # Eliminar cuenta por correo electrónico
    path('api/usuarios/me/eliminar_cuenta/', EliminarCuentaView.as_view(), name='eliminar_cuenta'),

    # Mapa
    path('contacto/', views.contacto_view, name='contacto'),

    # Transbank
    path('webpay/iniciar/', views.iniciar_pago, name='iniciar_pago'),
    path('webpay/respuesta/', views.respuesta_pago, name='respuesta_pago'),
]