import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import User
from properties.models import Property
from locations.models import Zone, Municipality


def parse_google_maps_url(url):
    """Extrae coordenadas de una URL de Google Maps."""
    # Formato: https://www.google.com/maps/@lat,lng,z
    match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if match:
        return float(match.group(1)), float(match.group(2))

    # Formato: /maps?q=lat,lng o /maps/search/?api=1&query=lat%2Clng
    match = re.search(r'[?&]q=(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if match:
        return float(match.group(1)), float(match.group(2))

    match = re.search(r'query=(-?\d+\.\d+)%2C(-?\d+\.\d+)', url)
    if match:
        return float(match.group(1)), float(match.group(2))

    # Formato: !3dlat!4dlng o /place/.../@lat,lng
    match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if match:
        return float(match.group(1)), float(match.group(2))

    return None, None


def home(request):
    """Página principal - vista pública para clientes."""
    zones = Zone.objects.prefetch_related('municipalities').order_by('order')
    properties = Property.objects.filter(status='published').select_related(
        'municipality', 'municipality__zone'
    ).prefetch_related('images')[:12]

    context = {
        'properties': properties,
        'zones': zones,
        'filters': {}
    }
    return render(request, 'home.html', context)


def map_view(request):
    """Vista del mapa interactivo con todas las propiedades."""
    properties = Property.objects.filter(
        status='published',
        latitude__isnull=False,
        longitude__isnull=False
    ).select_related('municipality', 'published_by').prefetch_related('images')

    properties_data = []
    for p in properties:
        primary_image = p.images.filter(is_primary=True).first() or p.images.first()
        properties_data.append({
            'id': p.id,
            'title': p.title,
            'price': float(p.price),
            'address': p.address,
            'property_type': p.property_type,
            'operation_type': p.operation_type,
            'latitude': float(p.latitude),
            'longitude': float(p.longitude),
            'image': primary_image.image.url if primary_image else None,
            'municipality': p.municipality.name,
        })

    context = {
        'properties': properties_data,
    }
    return render(request, 'map.html', context)


@login_required
def dashboard(request):
    """Dashboard después de login."""
    if request.user.is_admin():
        context = {
            'total_properties': Property.objects.count(),
            'total_vendors': User.objects.filter(role='vendedor').count(),
            'total_users': User.objects.count(),
        }
    else:
        context = {
            'my_properties': Property.objects.filter(published_by=request.user).count(),
        }
    return render(request, 'dashboard/base.html', context)