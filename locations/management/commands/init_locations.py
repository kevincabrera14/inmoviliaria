from django.core.management.base import BaseCommand

from locations.models import Zone, Municipality


class Command(BaseCommand):
    help = 'Crea las zonas y municipios del Valle de Aburrá'

    def handle(self, *args, **options):
        # Limpiar datos existentes
        Municipality.objects.all().delete()
        Zone.objects.all().delete()

        # Crear zonas
        norte = Zone.objects.create(name='Aburrá Norte', slug='aburra-norte', order=1)
        centro = Zone.objects.create(name='Aburrá Centro', slug='aburra-centro', order=2)
        sur = Zone.objects.create(name='Aburrá Sur', slug='aburra-sur', order=3)

        # Crear municipios
        municipalities_data = [
            # Norte
            ('Barbosa', 'barbosa', norte, 1),
            ('Girardota', 'girardota', norte, 2),
            ('Copacabana', 'copacabana', norte, 3),
            ('Bello', 'bello', norte, 4),
            # Centro
            ('Medellín', 'medellin', centro, 5),
            # Sur
            ('Envigado', 'envigado', sur, 6),
            ('Itagüí', 'itagui', sur, 7),
            ('Sabaneta', 'sabaneta', sur, 8),
            ('La Estrella', 'la-estrella', sur, 9),
            ('Caldas', 'caldas', sur, 10),
        ]

        for name, slug, zone, order in municipalities_data:
            Municipality.objects.create(name=name, slug=slug, zone=zone, order=order)
            self.stdout.write(f'  Creado: {name} ({zone.name})')

        self.stdout.write(self.style.SUCCESS(
            f'\n[OK] Creados {Zone.objects.count()} zonas y {Municipality.objects.count()} municipios'
        ))