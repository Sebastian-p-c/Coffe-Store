from django.db import models

# Create your models here.
class usuario(models.Model):
    username = models.CharField(max_length=20)
    clave = models.CharField(max_length=20)
    correo = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class carro(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.IntegerField()

    def __str__(self):
        return self.producto

