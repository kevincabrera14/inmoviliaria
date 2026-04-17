from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cedula')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Información adicional', {'fields': ('role', 'cedula', 'telefono', 'foto')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'cedula', 'telefono', 'is_active'),
        }),
    )

    actions = ['activate_vendors', 'deactivate_vendors']

    @admin.action(description='Activar vendedores seleccionados')
    def activate_vendors(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Desactivar vendedores seleccionados')
    def deactivate_vendors(self, request, queryset):
        queryset.update(is_active=False)