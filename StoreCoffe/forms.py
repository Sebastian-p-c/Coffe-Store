from django import forms
from .models import usuario
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

class RegistroUsuarioForm(forms.ModelForm):
    clave = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = usuario
        fields = ['username', 'correo', 'clave']
        
# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=20)
#     clave = forms.CharField(widget=forms.PasswordInput)

class AutheticationForms(forms.ModelForm):

    clave = forms.CharField(label="clave", widget=forms.PasswordInput)

    class Meta:
        model = usuario
        fields = ('username', 'clave')

    def clean(self):
        username = self.cleaned_data['username']
        clave = self.cleaned_data['clave']

        user = authenticate(username=username, password=clave)

        if user is None:
            raise forms.ValidationError("El usuario o clave son incorrectas")