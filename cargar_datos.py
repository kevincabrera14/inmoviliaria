import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from locations.models import Zone, Municipality

def limpiar_duplicados():
    """Encuentra y corrige municipios duplicados."""

    print("🔍 Buscando municipios duplicados...\n")

    # Encontrar todos los nombres duplicados
    from django.db.models import Count
    duplicados = Municipality.objects.values('name').annotate(
        count=Count('id')
    ).filter(count__gt=1)

    print(f"Municipios con nombres duplicados: {list(duplicados)}")

    # Zonas correctas
    zonas_data = {
        'Zona Norte': {'slug': 'zona-norte', 'order': 1},
        'Zona Centro': {'slug': 'zona-centro', 'order': 2},
        'Zona Sur': {'slug': 'zona-sur', 'order': 3},
    }

    # Crear o actualizar zonas
    zonas = {}
    for nombre, data in zonas_data.items():
        zona, created = Zone.objects.update_or_create(
            slug=data['slug'],
            defaults={'name': nombre, 'order': data['order']}
        )
        zonas[nombre] = zona
        print(f"{'✅' if created else '🔄'} Zona: {nombre}")

    # Mapping correcto de municipios a zonas
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

    # Procesar cada municipio duplicado
    for dup in duplicados:
        nombre = dup['name']
        muni_list = Municipality.objects.filter(name=nombre).order_by('pk')

        print(f"\n📍 {nombre} tiene {muni_list.count()} registros")

        # Mantener el primero, eliminar los demás
        primero = muni_list.first()
        print(f"   ✅ Manteniendo: pk={primero.pk}, slug={primero.slug}, zone={primero.zone.name}")

        # Asignar a la zona correcta
        zona_correcta = municipio_zonas.get(nombre)
        if zona_correcta:
            primero.zone = zonas[zona_correcta]
            primero.save()
            print(f"   🔄 Zona asignada: {zona_correcta}")

        # Eliminar duplicados
        for dup_muni in muni_list[1:]:
            # Contar propiedades antes de eliminar
            prop_count = dup_muni.properties.count()
            print(f"   🗑️ Eliminando duplicado: pk={dup_muni.pk}, slug={dup_muni.slug}, propiedades={prop_count}")

            if prop_count > 0:
                # Transferir propiedades al primero
                print(f"      ↪️ Moviendo {prop_count} propiedades al municipio principal...")
                from properties.models import Property
                Property.objects.filter(municipality=dup_muni).update(municipality=primero)

            dup_muni.delete()

    # Mostrar resultado final
    print("\n" + "="*50)
    print("🎉 RESULTADO FINAL:")
    print("="*50)
    for zona in Zone.objects.all().order_by('order'):
        print(f"\n{zona.name}:")
        for muni in zona.municipalities.all().order_by('order'):
            print(f"  - {muni.name} (slug: {muni.slug})")


if __name__ == '__main__':
    limpiar_duplicados()
