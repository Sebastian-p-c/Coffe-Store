from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Manager personalizado para crear usuarios y superusuarios
class UsuarioManager(BaseUserManager):
    def create_user(self, username, correo, password=None):
        if not correo:
            raise ValueError('El correo debe ser proporcionado')
        user = self.model(username=username, correo=correo)
        user.set_password(password)  # Usamos set_password para establecer la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, username, correo, password=None):
        user = self.create_user(username, correo, password)
        user.is_admin = True
        user.is_staff = True  # Hacer al superusuario un miembro del staff
        user.is_superuser = True  # El superusuario debe tener permisos completos
        user.save(using=self._db)
        return user


# Modelo personalizado de Usuario
class Usuario(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)  # Django manejará las contraseñas de manera segura
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Campo requerido por Django para acceder al admin
    is_superuser = models.BooleanField(default=False)  # Campo necesario para superusuarios

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'  # Campo por el cual los usuarios se autentican
    REQUIRED_FIELDS = ['correo']  # Otros campos obligatorios para crear un usuario

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # El superusuario tiene todos los permisos
        return self.is_admin or self.is_superuser

    def has_module_perms(self, app_label):
        # El superusuario tiene acceso a todos los módulos
        return self.is_admin or self.is_superuser

    def save(self, *args, **kwargs):
        # Aseguramos que si un usuario es superusuario, tenga acceso de staff
        if self.is_superuser:
            self.is_staff = True
        super().save(*args, **kwargs)


# Modelo de carrito (sin cambios)
class carro(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.IntegerField()

    def __str__(self):
        return self.producto
