from django import forms

from .models import Property, PropertyImage
from locations.models import Municipality


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