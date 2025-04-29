from django.db import models
import uuid
# Create your models here.
class usuario(models.Model):
    username = models.CharField(max_length=20)
    clave = models.CharField(max_length=20)
    correo = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class Transaccion(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    commerce_code = models.CharField(max_length=100)
    monto = models.FloatField()
    id_session = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, default='pendiente')
    
    def __str__(self):
        return self.token


class carro(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.IntegerField()

    def __str__(self):
        return self.producto

