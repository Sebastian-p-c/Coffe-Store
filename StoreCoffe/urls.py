from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import TransaccionViewSet

router = DefaultRouter()
router.register(r'transacciones', TransaccionViewSet, basename='transaccion')

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('detalleproducto/', views.detalleproducto, name='detalleproducto'),
    path("logout/", views.logout_view, name="logout"),
    path('api/', include(router.urls)),
]