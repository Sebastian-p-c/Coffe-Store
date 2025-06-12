from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from unittest.mock import patch
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from django.conf import settings


import re

class UsuarioTests(TestCase):

    # // PU001 //

    def setUp(self):
        # Crear un usuario de prueba
        self.username = "usuario1"
        self.correo = "usuario1@example.com"
        self.password = "1234"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            correo=self.correo,
            password=self.password
        )

        # Obtener token JWT inicial
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    # // PU002 //

    def test_inicio_sesion(self):
        # Intentar iniciar sesión con las credenciales correctas
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'usuario1', 'password': '1234'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verificar que el login es exitoso
        self.assertIn('access', response.data)  # Verificar que el token de acceso esté presente
    
    # // PU003 y PU004 //

    def test_modificar_contrasena(self):
        # Nueva contraseña
        nueva_contrasena = '5678'

        # Enviar una solicitud POST a la API de cambio de contraseña con la nueva contraseña
        response = self.client.post(reverse('cambiar_password'), {'nueva_clave': nueva_contrasena}, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verificar que la respuesta es 200 OK

        # Verificar que la contraseña haya sido actualizada
        self.user.refresh_from_db()  # Actualizamos el objeto de usuario
        self.assertTrue(self.user.check_password(nueva_contrasena))  # Verificar que la nueva contraseña esté correcta

        # Regenerar el token JWT con la nueva contraseña
        refresh = RefreshToken.for_user(self.user)
        new_access_token = str(refresh.access_token)  # Nuevo token con la nueva contraseña

        # Intentar iniciar sesión con la nueva contraseña (usando la nueva contraseña)
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'usuario1', 'password': nueva_contrasena})
        
        # Verificar que el login es exitoso con la nueva contraseña
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verificar que el login es exitoso
        self.assertIn('access', response.data)  # Verificar que el token de acceso esté presente

        # Verificar que el token tiene el formato adecuado de JWT (3 partes separadas por '.')
        self.assertTrue(re.match(r'^[\w-]+\.[\w-]+\.[\w-]+$', response.data['access']))  # Verificar formato JWT
        self.assertIsNotNone(response.data['access'])  # Verificar que el token de acceso no sea None

    # // PU005 //
    def test_inicio_sesion_contrasena_incorrecta(self):
            # Intentar iniciar sesión con la contraseña incorrecta
            response = self.client.post(reverse('token_obtain_pair'), {'username': 'usuario1', 'password': '11111'})
            
            # Verificar que el login falla con la contraseña incorrecta (código de estado 401)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Verificar que el login falla
            self.assertNotIn('access', response.data)  # Verificar que el token de acceso no esté presente
    
    # // PU006: Se comprueba en localhost, ya que son cargas de imagenes

    # // PU007 //
    def test_registro_usuario_duplicado(self):
        # Intentar registrar un nuevo usuario con las mismas credenciales
        data = {
            'username': 'usuario1',  # Mismo nombre de usuario
            'correo': 'usuario1@example.com',  # Mismo correo
            'password': '1234'  # Mismas credenciales
        }

        # Enviar una solicitud POST a la API de registro
        response = self.client.post(reverse('registro_api'), data, format='json')

        # Verificar que la respuesta sea un error 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verificar que los errores de validación sean los correctos (usuario o correo duplicados)
        self.assertIn('username', response.data)  # Verificar que el error de "username" esté presente
        self.assertIn('correo', response.data)  # Verificar que el error de "correo" esté presente

class TransbankTests(TestCase):

    def test_redireccionamiento_transbank_sandbox(self):
            # Llamamos a la URL para iniciar el pago
            response = self.client.post(reverse('iniciar_pago'), data={'producto': 'prod1'})

            # Verificar que la respuesta sea una redirección (302)
            self.assertEqual(response.status_code, 302)

            # Verificar que la URL de redirección comience con la URL de Transbank Sandbox
            self.assertTrue(response['Location'].startswith('https://webpay3gint.transbank.cl'))
    
    def test_cancelar_pago_y_redirigir(self):
        # Simulamos la respuesta de Transbank después de un pago cancelado
        # Usamos un token simulado para la prueba
        response = self.client.get(reverse('respuesta_pago'), {
            'TBK_TOKEN': '01ab90e73fe64327bdb3386590e8efb8b015d5dd6a15c4080948dd7aa073418d',
            'TBK_ORDEN_COMPRA': 'ORD-prod1',  # Orden de compra simulada
            'TBK_ID_SESION': 'session123',
            'cancel': 'true'  # Simulamos que el pago fue cancelado
        })

        # Verificar que la respuesta sea 200 OK (No es una redirección)
        self.assertEqual(response.status_code, 200)