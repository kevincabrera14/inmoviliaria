import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from locations.models import Zone, Municipality

def cargar_valle_de_aburra():
    # 1. Crear la Zona (si no existe)
    zona, created = Zone.objects.get_or_create(
        name="Valle de Aburrá", 
        slug="valle-de-aburra"
    )
    
    # 2. Lista de Municipios
    municipios = [
        "Medellín", "Bello", "Itagüí", "Envigado", "Sabaneta", 
        "Caldas", "La Estrella", "Girardota", "Copacabana", "Barbosa"
    ]
    
    for nombre in municipios:
        muni, created = Municipality.objects.get_or_create(
            name=nombre,
            zone=zona
        )
        if created:
            print(f"✅ Municipio creado: {nombre}")
        else:
            print(f"ℹ️ {nombre} ya existía.")

if __name__ == '__main__':
    cargar_valle_de_aburra()