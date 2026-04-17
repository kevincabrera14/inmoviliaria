from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import User
from properties.models import Property
from locations.models import Zone, Municipality


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