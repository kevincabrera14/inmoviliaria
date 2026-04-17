from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Property, PropertyImage
from locations.models import Zone, Municipality


def property_list(request):
    """Lista todas las propiedades publicadas."""
    properties = Property.objects.filter(status='published').select_related(
        'municipality', 'municipality__zone'
    ).prefetch_related('images')

    zones = Zone.objects.prefetch_related('municipalities').order_by('order')

    # Filtros
    property_type = request.GET.get('type')
    operation_type = request.GET.get('operation')
    zone_slug = request.GET.get('zone')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if property_type:
        properties = properties.filter(property_type=property_type)
    if operation_type:
        properties = properties.filter(operation_type=operation_type)
    if zone_slug:
        properties = properties.filter(municipality__zone__slug=zone_slug)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    context = {
        'properties': properties,
        'zones': zones,
        'filters': {
            'type': property_type,
            'operation': operation_type,
            'zone': zone_slug,
            'min_price': min_price,
            'max_price': max_price,
        }
    }
    return render(request, 'properties/list.html', context)


def property_list_by_municipality(request, slug):
    """Lista propiedades por municipio."""
    municipality = get_object_or_404(Municipality, slug=slug)
    properties = Property.objects.filter(
        municipality=municipality,
        status='published'
    ).select_related('municipality', 'municipality__zone').prefetch_related('images')

    zones = Zone.objects.prefetch_related('municipalities').order_by('order')

    context = {
        'properties': properties,
        'municipality': municipality,
        'zones': zones,
    }
    return render(request, 'properties/list.html', context)


def property_detail(request, pk):
    """Detalle de una propiedad."""
    prop = get_object_or_404(
        Property.objects.select_related('municipality', 'municipality__zone', 'published_by'),
        pk=pk
    )
    images = prop.images.all().order_by('order')
    related = Property.objects.filter(
        municipality=prop.municipality,
        status='published'
    ).exclude(pk=pk)[:4]

    context = {
        'property': prop,
        'images': images,
        'related': related,
    }
    return render(request, 'properties/detail.html', context)