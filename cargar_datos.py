import os
import django
import unicodedata
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from locations.models import Zone, Municipality


def normalize_slug(text):
    """Convierte texto a slug ASCII sin tildes ni caracteres especiales."""
    slug = unicodedata.normalize('NFD', text)
    slug = ''.join(c for c in slug if unicodedata.category(c) != 'Mn')
    slug = slug.lower().strip()
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug


def cargar_zonas():
    """Actualiza las zonas y municipios del Valle de Aburrá."""

    # Primero, crear o actualizar las zonas
    zonas_data = [
        {'name': 'Zona Norte', 'slug': 'zona-norte', 'order': 1},
        {'name': 'Zona Centro', 'slug': 'zona-centro', 'order': 2},
        {'name': 'Zona Sur', 'slug': 'zona-sur', 'order': 3},
    ]

    zonas = {}
    for zd in zonas_data:
        zona, created = Zone.objects.update_or_create(
            slug=zd['slug'],
            defaults={'name': zd['name'], 'order': zd['order']}
        )
        zonas[zd['name']] = zona
        print(f"{'✅' if created else '🔄'} Zona: {zona.name}")

    # Mapping de municipios a sus zonas
    municipio_zonas = {
        'Barbosa': 'Zona Norte',
        'Girardota': 'Zona Norte',
        'Copacabana': 'Zona Norte',
        'Bello': 'Zona Norte',
        'Medellín': 'Zona Centro',
        'Envigado': 'Zona Sur',
        'Itagüí': 'Zona Sur',
        'Sabaneta': 'Zona Sur',
        'La Estrella': 'Zona Sur',
        'Caldas': 'Zona Sur',
    }

    # Actualizar todos los slugs de municipios
    print("\n🔧 Corrigiendo slugs de municipios...")
    for muni in Municipality.objects.all():
        correct_slug = normalize_slug(muni.name)
        muni.slug = correct_slug
        muni.save()
        print(f"   {muni.name} -> slug: {correct_slug}")

    # Asignar municipios a zonas correctas
    print("\n📍 Asignando municipios a zonas...")
    for muni in Municipality.objects.all():
        zona_nombre = municipio_zonas.get(muni.name)
        if zona_nombre and muni.zone.name != zona_nombre:
            muni.zone = zonas[zona_nombre]
            muni.save()
            print(f"   {muni.name} -> {zona_nombre}")

    print("\n🎉 Completado!")
    print(f"Zonas: {Zone.objects.count()}")
    print(f"Municipios: {Municipality.objects.count()}")
    for zona in Zone.objects.all():
        muni_list = ', '.join([m.name for m in zona.municipalities.all()])
        print(f"  {zona.name}: {muni_list}")


if __name__ == '__main__':
    cargar_zonas()


if __name__ == '__main__':
    cargar_zonas()