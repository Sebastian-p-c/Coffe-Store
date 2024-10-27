from django import forms
from .models import usuario

class RegistroUsuarioForm(forms.ModelForm):
    clave = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = usuario
        fields = ['username', 'correo', 'clave']
