from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Definir 'password' como solo escritura

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'correo', 'password']  # Reemplazamos 'clave' por 'password'

    def create(self, validated_data):
        # Usar set_password para asegurar que la contraseña se almacene encriptada
        password = validated_data.pop('password', None)
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            correo=validated_data['correo'],
            password=password  # Usar el campo 'password'
        )
        return user

    def update(self, instance, validated_data):
        # Actualizar campos con encriptación de contraseña si es necesario
        instance.username = validated_data.get('username', instance.username)
        instance.correo = validated_data.get('correo', instance.correo)
        if 'password' in validated_data:  # Cambié 'clave' por 'password'
            instance.set_password(validated_data['password'])  # Encriptar nueva contraseña
        instance.save()
        return instance

