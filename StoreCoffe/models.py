from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self, username, correo, password=None):
        if not correo:
            raise ValueError('El correo debe ser proporcionado')
        user = self.model(username=username, correo=correo)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, correo, password=None):
        user = self.create_user(username, correo, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(max_length=255, unique=True)
    clave = models.CharField(max_length=128, default='temporal123')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['correo']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin



class carro(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.IntegerField()

    def __str__(self):
        return self.producto

