import os
import django
import unicodedata

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils.text import slugify
from locations.models import Zone, Municipality


def safe_slugify(text):
    """Convierte texto a slug ASCII sin tildes."""
    # Primero normalizar y eliminar tildes
    slug = unicodedata.normalize('NFD', text)
    slug = ''.join(c for c in slug if unicodedata.category(c) != 'Mn')
    # Luego usar slugify de Django que es más robusto
    return slugify(slug)


def cargar_zonas():
    """Actualiza las zonas y municipios del Valle de Aburrá."""

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

    # Primero crear o actualizar zonas
    zonas = {}
    for nombre, slug in [('Zona Norte', 'zona-norte'), ('Zona Centro', 'zona-centro'), ('Zona Sur', 'zona-sur')]:
        zona, created = Zone.objects.update_or_create(
            slug=slug,
            defaults={'name': nombre, 'order': list(municipio_zonas.values()).count(nombre)}
        )
        zonas[nombre] = zona
        print(f"{'✅' if created else '🔄'} Zona: {nombre}")

    # Recolectar slugs usados para evitar duplicados
    used_slugs = set(Municipality.objects.values_list('slug', flat=True))
    print(f"\nSlugs ya usados: {used_slugs}")

    # Actualizar municipios uno por uno
    print("\n🔧 Actualizando municipios...")
    for muni in Municipality.objects.all():
        # Buscar la zona correcta
        zona_nombre = municipio_zonas.get(muni.name)
        if zona_nombre:
            muni.zone = zonas[zona_nombre]
            print(f"   📍 {muni.name} -> {zona_nombre}")

        # Generar slug limpio
        new_slug = safe_slugify(muni.name)

        # Si el slug ya existe y es de otro municipio, agregar su ID
        if new_slug in used_slugs:
            other = Municipality.objects.filter(slug=new_slug).first()
            if other and other.pk != muni.pk:
                # Crear slug único
                new_slug = f"{new_slug}-{muni.pk}"
                print(f"      ⚠️Slug duplicado, usando: {new_slug}")

        muni.slug = new_slug
        muni.save()
        used_slugs.add(new_slug)
        print(f"      ✅ slug: {new_slug}")

    print("\n🎉 Completado!")
    print(f"Zonas: {Zone.objects.count()}")
    print(f"Municipios: {Municipality.objects.count()}")
    for zona in Zone.objects.all().order_by('order'):
        muni_list = ', '.join([m.name for m in zona.municipalities.all().order_by('order')])
        print(f"  {zona.name}: {muni_list}")


if __name__ == '__main__':
    cargar_zonas()


if __name__ == '__main__':
    cargar_zonas()