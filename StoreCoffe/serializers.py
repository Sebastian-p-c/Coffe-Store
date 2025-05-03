# serializers.py
from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'correo', 'clave']

    def create(self, validated_data):
        # Usar set_password para asegurar que la clave se almacene encriptada
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            correo=validated_data['correo'],
            password=validated_data['clave']
        )
        return user

    def update(self, instance, validated_data):
        # Actualizar campos con encriptación de contraseña si es necesario
        instance.username = validated_data.get('username', instance.username)
        instance.correo = validated_data.get('correo', instance.correo)
        if 'clave' in validated_data:
            instance.set_password(validated_data['clave'])  # Encriptar nueva clave
        instance.save()
        return instance

