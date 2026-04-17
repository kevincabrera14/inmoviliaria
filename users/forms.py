from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class LoginForm(AuthenticationForm):
    """Formulario de login personalizado."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario',
            'autofocus': True
        })
    )
    password = forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña'
    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    'Usuario o contraseña incorrectos.',
                    code='invalid_login'
                )
            if not self.user_cache.is_active:
                raise forms.ValidationError(
                    'Esta cuenta está desactivada.',
                    code='inactive'
                )
        return self.cleaned_data