from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cedula')
    ordering = ('-date_joined',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('role', 'cedula', 'telefono', 'foto')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('role', 'cedula', 'telefono')}),
    )

    actions = ['activar_vendedores', 'desactivar_vendedores']

    @admin.action(description='Activar vendedores seleccionados')
    def activar_vendedores(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Desactivar vendedores seleccionados')
    def desactivar_vendedores(self, request, queryset):
        queryset.update(is_active=False)