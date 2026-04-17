import os
import django
from django.utils.text import slugify # Importante para el slug

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from locations.models import Zone, Municipality

def cargar_valle_de_aburra():
    # 1. Crear la Zona
    zona, created = Zone.objects.get_or_create(
        name="Valle de Aburrá", 
        defaults={'slug': 'valle-de-aburra'}
    )
    
    # 2. Lista de Municipios
    municipios = [
        "Medellín", "Bello", "Itagüí", "Envigado", "Sabaneta", 
        "Caldas", "La Estrella", "Girardota", "Copacabana", "Barbosa"
    ]
    
    for nombre in municipios:
        # Generamos el slug a partir del nombre (ej: "La Estrella" -> "la-estrella")
        muni_slug = slugify(nombre)
        
        muni, created = Municipality.objects.get_or_create(
            name=nombre,
            zone=zona,
            defaults={'slug': muni_slug} # Esto evita el error de duplicado
        )
        
        if created:
            print(f"✅ Municipio creado: {nombre}")
        else:
            print(f"ℹ️ {nombre} ya existía.")

if __name__ == '__main__':
    cargar_valle_de_aburra()