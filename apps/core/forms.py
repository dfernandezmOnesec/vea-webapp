from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


# -------------------------------
# Formulario de Registro (Signup)
# -------------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "username")
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Tu apellido'}),
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario (opcional)'}),
        }


# ---------------------------------------------
# Formulario de Inicio de Sesión (Login Custom)
# ---------------------------------------------
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'placeholder': 'correo@ejemplo.com',
        })
    )
