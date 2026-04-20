import os
import django
import unicodedata

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from locations.models import Zone, Municipality


def normalize_slug(text):
    """Convierte texto a slug ASCII sin tildes ni caracteres especiales."""
    # Normalizar a forma decomposed (NFD) y eliminar marcas diacríticas
    slug = unicodedata.normalize('NFD', text)
    slug = ''.join(c for c in slug if unicodedata.category(c) != 'Mn')
    # Convertir espacios y caracteres especiales a guiones
    slug = slug.lower().replace(' ', '-')
    # Eliminar caracteres que no sean letras, números o guiones
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    return slug


def cargar_zonas():
    """Carga las 3 zonas del Valle de Aburrá con sus municipios."""

    # Definir zonas y municipios (ordenados de norte a sur)
    zonas_data = [
        {
            'name': 'Zona Norte',
            'slug': 'zona-norte',
            'order': 1,
            'municipios': [
                ('Barbosa', 1),
                ('Girardota', 2),
                ('Copacabana', 3),
                ('Bello', 4),
            ]
        },
        {
            'name': 'Zona Centro',
            'slug': 'zona-centro',
            'order': 2,
            'municipios': [
                ('Medellín', 1),
            ]
        },
        {
            'name': 'Zona Sur',
            'slug': 'zona-sur',
            'order': 3,
            'municipios': [
                ('Envigado', 1),
                ('Itagüí', 2),
                ('Sabaneta', 3),
                ('La Estrella', 4),
                ('Caldas', 5),
            ]
        },
    ]

    # Crear o actualizar zonas
    for zona_data in zonas_data:
        zona, created = Zone.objects.update_or_create(
            slug=zona_data['slug'],
            defaults={
                'name': zona_data['name'],
                'order': zona_data['order']
            }
        )
        print(f"{'✅' if created else '🔄'} Zona {'creada' if created else 'actualizada'}: {zona.name}")

        # Crear o actualizar municipios
        for muni_nombre, muni_order in zona_data['municipios']:
            muni_slug = normalize_slug(muni_nombre)
            muni, created = Municipality.objects.update_or_create(
                slug=muni_slug,
                defaults={
                    'name': muni_nombre,
                    'zone': zona,
                    'order': muni_order
                }
            )
            print(f"   {'✅' if created else '🔄'} Municipio {'creado' if created else 'actualizado'}: {muni.name} -> slug: {muni_slug}")

    print("\n🎉 Carga completada!")
    print(f"Total zonas: {Zone.objects.count()}")
    print(f"Total municipios: {Municipality.objects.count()}")


if __name__ == '__main__':
    cargar_zonas()