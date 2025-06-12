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


class UsuarioTests(TestCase):
    
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

        # Obtener token JWT
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_login_url(self):
        # Verificar que la URL de login devuelve un código de estado 200
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_registro_url(self):
        # Verificar que la URL de registro devuelve un código de estado 200
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        # Verificar que la URL de logout redirige correctamente
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_api_token_obtain(self):
        # Verificar que la URL para obtener el token JWT devuelve un código de estado 200
        response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Verifica que el token de acceso esté presente

    def test_api_token_refresh(self):
        # Primero, obtener el token de acceso
        refresh_token = RefreshToken.for_user(self.user)
        response = self.client.post(reverse('token_refresh'), {'refresh': str(refresh_token)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Verifica que el token de acceso se refresque

    def test_api_registro_usuario(self):
        # Verificar que la API de registro de usuario funcione correctamente
        data = {
            'username': 'usuario_api',
            'correo': 'usuario_api@example.com',
            'password': 'api_pass'
        }
        response = self.client.post(reverse('registro_api'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['correo'], data['correo'])

    def test_api_obtener_usuario(self):
        # Verificar que la API para obtener los datos del usuario autenticado funcione correctamente
        response = self.client.get(reverse('usuario-me'), HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.username)

    def test_api_cambiar_contrasena(self):
        # Cambiar la contraseña con autenticación
        data = {'nueva_clave': 'nueva_contrasena'}
        response = self.client.post(reverse('cambiar_password'), data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que la nueva contraseña sea válida
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('nueva_contrasena'))

    def test_api_eliminar_cuenta(self):
        # Eliminar cuenta con autenticación
        response = self.client.delete(reverse('eliminar_cuenta'), HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verificar que el usuario haya sido eliminado
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(username=self.username)

    def test_restriccion_registro_usuario_existente(self):
        # Intentar crear un usuario con las mismas credenciales
        data = {
            'username': self.username,
            'correo': self.correo,
            'password': 'new_password'
        }
        response = self.client.post(reverse('registro_api'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # El usuario ya existe


class TransbankTests(TestCase):

    def setUp(self):
        # Crear un usuario de prueba para los pagos
        self.username = "usuario_pago"
        self.correo = "usuario_pago@example.com"
        self.password = "1234"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            correo=self.correo,
            password=self.password
        )

        # Obtener token JWT
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    @patch.object(Transaction, 'create', return_value={'url': 'http://127.0.0.1/webpay', 'token': 'mocked_token'})
    def test_iniciar_pago_url(self, mock_create):
        # Verificar que la URL para iniciar el pago de Transbank devuelva un código de estado 200
        response = self.client.get(reverse('iniciar_pago'), HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 302)  # Redirección al URL de pago de Transbank
        self.assertEqual(response['Location'], 'http://127.0.0.1/webpay?token_ws=mocked_token')

    @patch.object(Transaction, 'commit', return_value={'status': 'success', 'buy_order': 'ORD123', 'amount': 3000})
    def test_respuesta_pago_url(self, mock_commit):
        # Verificar que la URL de respuesta de pago de Transbank devuelva un código de estado 200
        response = self.client.get(reverse('respuesta_pago') + '?token_ws=mocked_token', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'status: success')

    @patch.object(Transaction, 'create', return_value={'url': 'http://127.0.0.1/webpay', 'token': 'mocked_token'})
    @patch.object(Transaction, 'commit', return_value={'status': 'success', 'buy_order': 'ORD123', 'amount': 3000})
    def test_transbank_proceso_pago(self, mock_commit, mock_create):
        # Test completo para simular un pago con Transbank
        response = self.client.get(reverse('iniciar_pago'), HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 302)  # Redirección al pago
        self.assertEqual(response['Location'], 'http://127.0.0.1/webpay?token_ws=mocked_token')

        # Simulación de la respuesta del pago
        response = self.client.get(reverse('respuesta_pago') + '?token_ws=mocked_token', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'status: success')


class ProductoTests(TestCase):

    def test_detalleproducto_url(self):
        # Verificar que la URL de detalle del producto devuelve un código de estado 200
        response = self.client.get(reverse('detalleproducto'))
        self.assertEqual(response.status_code, 200)

    def test_cafedivino_url(self):
        # Verificar que la URL de cafedivino devuelve un código de estado 200
        response = self.client.get(reverse('cafedivino'))
        self.assertEqual(response.status_code, 200)

    def test_cafeelite_url(self):
        # Verificar que la URL de cafeelite devuelve un código de estado 200
        response = self.client.get(reverse('cafeelite'))
        self.assertEqual(response.status_code, 200)

    def test_cafegolden_url(self):
        # Verificar que la URL de cafegolden devuelve un código de estado 200
        response = self.client.get(reverse('cafegolden'))
        self.assertEqual(response.status_code, 200)

    def test_cafehacking_url(self):
        # Verificar que la URL de cafehacking devuelve un código de estado 200
        response = self.client.get(reverse('cafehacking'))
        self.assertEqual(response.status_code, 200)

    def test_cafepower_url(self):
        # Verificar que la URL de cafepower devuelve un código de estado 200
        response = self.client.get(reverse('cafepower'))
        self.assertEqual(response.status_code, 200)

    def test_cafepremium_url(self):
        # Verificar que la URL de cafepremium devuelve un código de estado 200
        response = self.client.get(reverse('cafepremium'))
        self.assertEqual(response.status_code, 200)

    def test_cafeultimate_url(self):
        # Verificar que la URL de cafeultimate devuelve un código de estado 200
        response = self.client.get(reverse('cafeultimate'))
        self.assertEqual(response.status_code, 200)

    def test_cafeultimateplatino_url(self):
        # Verificar que la URL de cafeultimateplatino devuelve un código de estado 200
        response = self.client.get(reverse('cafeultimateplatino'))
        self.assertEqual(response.status_code, 200)

    def test_cafeultimatepremium_url(self):
        # Verificar que la URL de cafeultimatepremium devuelve un código de estado 200
        response = self.client.get(reverse('cafeultimatepremium'))
        self.assertEqual(response.status_code, 200)
