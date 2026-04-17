from django.db import models


class Zone(models.Model):
    """Zonas geográficas del Valle de Aburrá."""

    name = models.CharField('Nombre', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Municipality(models.Model):
    """Municipios del Valle de Aburrá."""

    name = models.CharField('Nombre', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    zone = models.ForeignKey(
        Zone,
        on_delete=models.CASCADE,
        related_name='municipalities'
    )
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name