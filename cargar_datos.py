import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from locations.models import Zone, Municipality

def cargar_zonas():
    """Carga las 3 zonas del Valle de Aburrá con sus municipios."""

    # Definir zonas y municipios (ordenados de norte a sur)
    zonas_data = [
        {
            'name': 'Zona Norte',
            'slug': 'zona-norte',
            'order': 1,
            'municipios': [
                ('Barbosa', 1),      # Más al norte
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
                ('Medellín', 1),     # Municipio núcleo
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
                ('Caldas', 5),       # Más al sur, donde nace el río Medellín
            ]
        },
    ]

    for zona_data in zonas_data:
        zona, created = Zone.objects.get_or_create(
            slug=zona_data['slug'],
            defaults={
                'name': zona_data['name'],
                'order': zona_data['order']
            }
        )

        if created:
            print(f"✅ Zona creada: {zona.name}")
        else:
            print(f"ℹ️ Zona ya existía: {zona.name}")

        for muni_nombre, muni_order in zona_data['municipios']:
            muni_slug = slugify(muni_nombre)
            muni, created = Municipality.objects.get_or_create(
                slug=muni_slug,
                defaults={
                    'name': muni_nombre,
                    'zone': zona,
                    'order': muni_order
                }
            )

            if created:
                print(f"   ✅ Municipio creado: {muni_nombre}")
            else:
                print(f"   ℹ️ {muni_nombre} ya existía.")


if __name__ == '__main__':
    cargar_zonas()