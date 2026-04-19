import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from locations.models import Zone, Municipality

def cargar_zonas():
    """Carga las 3 zonas del Valle de Aburrá con sus municipios."""

    # Eliminar datos anteriores
    Municipality.objects.all().delete()
    Zone.objects.all().delete()
    print("🗑️ Datos anteriores eliminados")

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

    for zona_data in zonas_data:
        zona = Zone.objects.create(
            name=zona_data['name'],
            slug=zona_data['slug'],
            order=zona_data['order']
        )
        print(f"✅ Zona creada: {zona.name}")

        for muni_nombre, muni_order in zona_data['municipios']:
            muni = Municipality.objects.create(
                name=muni_nombre,
                slug=muni_nombre.lower().replace(' ', '-').replace('í', 'i').replace('á', 'a'),
                zone=zona,
                order=muni_order
            )
            print(f"   ✅ Municipio: {muni.name} ({zona.name})")

    print("\n🎉 Carga completada!")
    print(f"Total zonas: {Zone.objects.count()}")
    print(f"Total municipios: {Municipality.objects.count()}")


if __name__ == '__main__':
    cargar_zonas()