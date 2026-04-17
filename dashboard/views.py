from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from users.models import User
from properties.models import Property


class DashboardMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixins para dashboard."""

    def test_func(self):
        return self.request.user.is_vendedor()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        return redirect('home')


class AdminRequiredMixin(UserPassesTestMixin):
    """Solo admin puede acceder."""

    def test_func(self):
        return self.request.user.is_admin()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        return redirect('dashboard:dashboard')


class AdminOrVendorMixin(UserPassesTestMixin):
    """Admin o vendedor."""

    def test_func(self):
        return self.request.user.is_vendedor()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        return redirect('home')


class DashboardView(AdminOrVendorMixin, View):
    """Dashboard principal."""

    def get(self, request):
        if request.user.is_admin():
            return render(request, 'dashboard/admin/dashboard.html')
        return render(request, 'dashboard/vendor/dashboard.html')


class VendorPropertyListView(AdminOrVendorMixin, View):
    """Lista de propiedades del vendedor."""

    def get(self, request):
        if request.user.is_admin():
            properties = Property.objects.select_related(
                'municipality', 'published_by'
            ).order_by('-created_at')
        else:
            properties = Property.objects.filter(
                published_by=request.user
            ).select_related('municipality').order_by('-created_at')

        return render(request, 'dashboard/vendor/property_list.html', {
            'properties': properties
        })


class VendorPropertyCreateView(AdminOrVendorMixin, View):
    """Crear propiedad."""

    def get(self, request):
        return render(request, 'dashboard/vendor/property_form.html')

    def post(self, request):
        # Crear propiedad
        pass