from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from properties.models import Property, PropertyImage
from properties.forms import PropertyForm, PropertyImageForm


@login_required
def vendor_property_list(request):
    """Lista de propiedades del vendedor."""
    if request.user.is_admin():
        properties = Property.objects.select_related('municipality', 'published_by').order_by('-created_at')
    else:
        properties = Property.objects.filter(published_by=request.user).select_related('municipality').order_by('-created_at')

    return render(request, 'dashboard/vendor/property_list.html', {
        'properties': properties
    })


@login_required
def vendor_property_create(request):
    """Crear propiedad."""
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.published_by = request.user
            property_obj.save()

            # Manejar imágenes múltiples
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                PropertyImage.objects.create(
                    property=property_obj,
                    image=image,
                    order=i,
                    is_primary=(i == 0)
                )

            messages.success(request, 'Propiedad creada exitosamente.')
            return redirect('dashboard:property_list')
    else:
        form = PropertyForm()

    return render(request, 'dashboard/vendor/property_form.html', {
        'form': form,
        'action': 'Crear'
    })


@login_required
def vendor_property_edit(request, pk):
    """Editar propiedad."""
    property_obj = get_object_or_404(Property, pk=pk)

    # Verificar permisos
    if not request.user.is_admin() and property_obj.published_by != request.user:
        messages.error(request, 'No tienes permiso para editar esta propiedad.')
        return redirect('dashboard:property_list')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()

            # Eliminar imágenes marcadas
            removed_ids = request.POST.getlist('removed_images')
            if removed_ids:
                PropertyImage.objects.filter(pk__in=removed_ids, property=property_obj).delete()

            # Agregar nuevas imágenes
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                PropertyImage.objects.create(
                    property=property_obj,
                    image=image,
                    order=property_obj.images.count() + i
                )

            messages.success(request, 'Propiedad actualizada exitosamente.')
            return redirect('dashboard:property_list')
    else:
        form = PropertyForm(instance=property_obj)

    return render(request, 'dashboard/vendor/property_form.html', {
        'form': form,
        'property': property_obj,
        'action': 'Editar'
    })


@login_required
def vendor_property_delete(request, pk):
    """Eliminar propiedad."""
    property_obj = get_object_or_404(Property, pk=pk)

    if not request.user.is_admin() and property_obj.published_by != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta propiedad.')
        return redirect('dashboard:property_list')

    property_obj.delete()
    messages.success(request, 'Propiedad eliminada exitosamente.')
    return redirect('dashboard:property_list')