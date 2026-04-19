from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', include('users.urls')),
    path('adminapp/', admin.site.urls),
    path('propiedades/', include('properties.urls')),
    path('dashboard/', include('dashboard.urls')),
]

# Servir archivos media en producción
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]