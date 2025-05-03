# auth_backend.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Busca al usuario con el nombre de usuario
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return None

        # Verifica la contraseña
        if check_password(password, user.clave):
            return user
        return None
