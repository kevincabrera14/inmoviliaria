import os
import django

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
            muni_slug = muni_nombre.lower().replace(' ', '-').replace('í', 'i').replace('á', 'a').replace('é', 'e')
            muni, created = Municipality.objects.update_or_create(
                slug=muni_slug,
                defaults={
                    'name': muni_nombre,
                    'zone': zona,
                    'order': muni_order
                }
            )
            print(f"   {'✅' if created else '🔄'} Municipio {'creado' if created else 'actualizado'}: {muni.name} ({zona.name})")

    print("\n🎉 Carga completada!")
    print(f"Total zonas: {Zone.objects.count()}")
    print(f"Total municipios: {Municipality.objects.count()}")


if __name__ == '__main__':
    cargar_zonas()