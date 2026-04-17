from django.contrib import admin
from django.utils.html import format_html

from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'is_primary', 'order')
    ordering = ('order',)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'municipality', 'property_type', 'operation_type', 'price', 'status', 'published_by', 'created_at')
    list_filter = ('status', 'property_type', 'operation_type', 'municipality__zone', 'municipality')
    search_fields = ('title', 'description', 'address')
    ordering = ('-created_at',)
    inlines = [PropertyImageInline]

    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'description', 'status')
        }),
        ('Detalles', {
            'fields': ('property_type', 'operation_type', 'price', 'area', 'rooms', 'bathrooms')
        }),
        ('Ubicación', {
            'fields': ('address', 'municipality')
        }),
        ('Características', {
            'fields': ('features',)
        }),
        ('Publicación', {
            'fields': ('published_by',)
        }),
    )

    actions = ['publish_properties', 'unpublish_properties']

    @admin.action(description='Publicar propiedades seleccionadas')
    def publish_properties(self, request, queryset):
        queryset.update(status='published')

    @admin.action(description='Despublicar propiedades seleccionadas')
    def unpublish_properties(self, request, queryset):
        queryset.update(status='draft')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.published_by = request.user
        super().save_model(request, obj, form, change)