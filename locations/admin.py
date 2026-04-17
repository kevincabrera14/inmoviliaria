from django.contrib import admin

from .models import Zone, Municipality


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'slug', 'order')
    list_filter = ('zone',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)