# Django
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Usuario custom con roles para el sistema inmobiliario."""

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        VENDEDOR = 'vendedor', 'Vendedor'
        CLIENTE = 'cliente', 'Cliente'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENTE
    )
    cedula = models.CharField(
        'Cédula',
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text='Cédula de ciudadanía colombiana'
    )
    telefono = models.CharField(
        'Teléfono',
        max_length=20,
        blank=True,
        help_text='Número de contacto WhatsApp'
    )
    foto = models.ImageField(
        'Foto de perfil',
        upload_to='users/fotos/',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_vendedor(self):
        return self.role in [self.Role.VENDEDOR, self.Role.ADMIN]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"