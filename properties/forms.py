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

    # Campo auxiliar para la URL de Google Maps
    maps_url = forms.CharField(
        label='Ubicación en Google Maps',
        required=False,
        help_text='Pega aquí la URL de Google Maps o las coordenadas (lat, lng) para ubicar la propiedad en el mapa.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://www.google.com/maps/@6.2442,-75.5812,15z o -6.2442, -75.5812'
        })
    )

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
            'area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'municipality': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['municipality'].queryset = Municipality.objects.select_related('zone').order_by('zone__order', 'order')

        # Si estamos editando, pre-llenar el campo maps_url con las coordenadas
        if self.instance and self.instance.pk:
            if self.instance.latitude and self.instance.longitude:
                self.initial['maps_url'] = f"{self.instance.latitude},{self.instance.longitude}"

    def clean_maps_url(self):
        url = self.cleaned_data.get('maps_url', '')
        if url:
            lat, lng = parse_google_maps_url(url)
            if lat is None:
                raise forms.ValidationError('No se pudieron extraer coordenadas de la URL. Asegúrate de que sea una URL válida de Google Maps o coordenadas (lat, lng).')
            self.cleaned_data['latitude'] = lat
            self.cleaned_data['longitude'] = lng
        return url

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Guardar coordenadas si fueron proporcionadas
        if 'latitude' in self.cleaned_data:
            instance.latitude = self.cleaned_data['latitude']
        if 'longitude' in self.cleaned_data:
            instance.longitude = self.cleaned_data['longitude']

        if commit:
            instance.save()
        return instance


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