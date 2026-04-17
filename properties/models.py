from django.db import models

from users.models import User
from locations.models import Municipality


class Property(models.Model):
    """Propiedad inmobiliaria."""

    class PropertyType(models.TextChoices):
        CASA = 'casa', 'Casa'
        APARTAMENTO = 'apartamento', 'Apartamento'
        TERRENO = 'terreno', 'Terreno'
        LOCAL = 'local', 'Local'
        OFICINA = 'oficina', 'Oficina'

    class OperationType(models.TextChoices):
        VENTA = 'venta', 'Venta'
        ARRIENDO = 'arriendo', 'Arriendo'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Borrador'
        PUBLISHED = 'published', 'Publicada'
        SOLD = 'sold', 'Vendida'
        RENTED = 'rented', 'Arrendada'

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')
    price = models.DecimalField('Precio', max_digits=12, decimal_places=2)
    property_type = models.CharField(
        'Tipo',
        max_length=20,
        choices=PropertyType.choices
    )
    operation_type = models.CharField(
        'Operación',
        max_length=20,
        choices=OperationType.choices
    )
    area = models.DecimalField(
        'Área (m²)',
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    rooms = models.PositiveIntegerField('Habitaciones', null=True, blank=True)
    bathrooms = models.PositiveIntegerField('Baños', null=True, blank=True)
    address = models.CharField('Dirección', max_length=300)
    latitude = models.DecimalField(
        'Latitud',
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        'Longitud',
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.PROTECT,
        related_name='properties'
    )
    features = models.JSONField(
        'Características adicionales',
        default=dict,
        blank=True
    )
    published_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='properties'
    )
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.municipality}"


class PropertyImage(models.Model):
    """Imagen de una propiedad."""

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField('Imagen', upload_to='properties/')
    is_primary = models.BooleanField('Imagen principal', default=False)
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imágenes'
        ordering = ['order']

    def __str__(self):
        return f"Imagen {self.order} - {self.property}"