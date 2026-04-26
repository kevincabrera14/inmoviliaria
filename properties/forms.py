from django import forms
import re

from .models import Property, PropertyImage
from locations.models import Municipality


def parse_google_maps_url(url):
    """Extrae coordenadas de una URL de Google Maps."""
    if not url:
        return None, None

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

    # Formato de coordenadas directo: -6.2442,-75.5812
    match = re.search(r'^(-?\d+\.\d+),(-?\d+\.\d+)$', url.strip())
    if match:
        return float(match.group(1)), float(match.group(2))

    return None, None


class PropertyForm(forms.ModelForm):
    """Formulario para crear/editar propiedades."""

    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'property_type', 'operation_type',
            'area', 'rooms', 'bathrooms', 'address', 'municipality', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'operation_type': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 234, 234-250, Aprox. 234 m²'}),
            'rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'municipality': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['municipality'].queryset = Municipality.objects.select_related('zone').order_by('zone__order', 'order')


class PropertyImageForm(forms.ModelForm):
    """Formulario para subir imágenes."""

    class Meta:
        model = PropertyImage
        fields = ['image', 'is_primary', 'order']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }