from django.urls import path

from . import views, views_properties

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('propiedades/', views_properties.vendor_property_list, name='property_list'),
    path('propiedades/crear/', views_properties.vendor_property_create, name='property_create'),
    path('propiedades/<int:pk>/editar/', views_properties.vendor_property_edit, name='property_edit'),
    path('propiedades/<int:pk>/eliminar/', views_properties.vendor_property_delete, name='property_delete'),
]