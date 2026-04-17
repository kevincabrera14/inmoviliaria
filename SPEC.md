# Sistema Inmobiliario - El Valle de Aburrá

## 1. Concepto & Visión

Plataforma inmobiliaria para gestionar propiedades en los 10 municipios del Valle de Aburrá (Antioquia, Colombia). Sistema robusto con roles diferenciados: admins gestionan vendedores, vendedores publican propiedades, clientes navegan sin registro. Interfaz limpia centrada en la ubicación geográfica.

## 2. Arquitectura

### Stack
- **Backend**: Django 5 + Django REST Framework
- **Base de datos**: PostgreSQL (Railway)
- **Almacenamiento imágenes**: WhiteNoise o Cloudinary
- **Deployment**: Railway

### Estructura de Apps
```
core/
├── users/           # Modelo User custom, auth, roles
├── properties/      # Modelo Property, imágenes, CRUD
├── locations/       # Modelo Municipality, Zone
└── core/           # Configuración principal, URLs, settings
```

## 3. Modelos

### User (extend Django AbstractUser)
- `role`: choices [admin, vendedor, cliente]
- `cedula`: string único (cédula colombiana)
- `telefono`: string opcional
- `is_active`: boolean

### Zone
- `name`: string (Aburrá Norte, Centro, Sur)
- `order`: int para ordenamiento

### Municipality
- `name`: string (Medellín, Bello, Envigado, etc.)
- `zone`: ForeignKey a Zone
- `slug`: string único para URL
- `order`: int para ordenamiento

### Property
- `title`: string
- `description`: text
- `price`: decimal
- `property_type`: choices [casa, apartamento, terreno, local, oficina]
- `operation_type`: choices [venta, arriendo]
- `area`: decimal (metros cuadrados)
- `rooms`: int
- `bathrooms`: int
- `address`: string
- `municipality`: ForeignKey a Municipality
- `features`: JSONField (parking, pool, etc.)
- `images`: ManyToMany a PropertyImage
- `published_by`: ForeignKey a User (vendedor)
- `status`: choices [draft, published, sold, rented]
- `created_at`, `updated_at`: datetime

### PropertyImage
- `property`: ForeignKey a Property
- `image`: ImageField
- `is_primary`: boolean
- `order`: int

## 4. Roles & Permisos

### Admin
- CRUD completo de vendedores
- Ver todas las propiedades
- Activar/desactivar vendedores
- Dashboard completo

### Vendedor
- CRUD de sus propias propiedades
- Subir imágenes múltiples
- Cambiar estado (draft/published)
- Solo ve sus propiedades

### Cliente
- Vista pública sin login
- Filtro por municipio/zona
- Filtro por tipo, precio, operación
- Ver detalle de propiedad
- Contacto (email/WhatsApp)

## 5. Vistas Pública (Cliente - sin login)

### Página Principal
- Header con logo, navegación por zonas
- Hero con búsqueda rápida
- Grid de propiedades recientes
- Filtros: zona, municipio, tipo, operación, rango precio

### Vista por Municipio
- `/propiedades/<municipio>/` - lista filtrada
- Template agrupado por zona (Norte, Centro, Sur)
- Sidebar con filtros
- Paginación

### Detalle Propiedad
- Galería de imágenes
- Toda la información
- Botón contacto (email o WhatsApp)
- Propiedades relacionadas

## 6. Admin/Vendedor Dashboard

### Admin
- Lista vendedores con estado
- Estadísticas del sistema
- Todas las propiedades

### Vendedor
- Mis propiedades
- Crear/editar propiedad
- Subir imágenes (drag & drop)
- Preview antes de publicar

## 7. URLs

```
# Público
/                           # Landing con propiedades
/propiedades/<municipio>/    # Por municipio
/propiedad/<id>/            # Detalle

# Auth
/login/
/logout/

# Admin (solo admin)
/admin/dashboard/
/admin/vendedores/
/admin/vendedores/add/

# Vendedor (admin y vendedor)
/dashboard/                 # Panel principal
/propiedades/mis-propiedades/
/propiedades/crear/
/propiedades/<id>/editar/
/propiedades/<id>/eliminar/
```

## 8. Templates

```
templates/
├── base.html
├── home.html
├── properties/
│   ├── list.html          # Lista pública
│   ├── detail.html        # Detalle
│   └── filter.html        # Filtros sidebar
├── dashboard/
│   ├── base.html
│   ├── admin/
│   │   └── dashboard.html
│   └── vendor/
│       ├── dashboard.html
│       └── property_form.html
├── users/
│   ├── login.html
│   └── profile.html
└── partials/
    ├── header.html
    ├── footer.html
    ├── property_card.html
    └── pagination.html
```

## 9. Variables de Entorno (.env)

```
DEBUG=False
SECRET_KEY=...
DATABASE_URL=postgres://...
ALLOWED_HOSTS=.railway.app
EMAIL_HOST=smtp.mailgun.org
EMAIL_FROM=contacto@inmobiliaria.com
WHATSAPP_NUMBER=+573001234567
```

## 10.部署 Railway

- `runtime.txt`: python-3.11
- `requirements.txt`: Django, gunicorn, whitenoise, psycopg2-binary, dj-database-url
- `railway.json`: configuración de servicio
- `.gitignore`: excludes __pycache__, .env, *.pyc

## 11.优先级 de implementación

1. **Fase 1**: Modelos, admin Django, autenticación
2. **Fase 2**: CRUD propiedades con imágenes
3. **Fase 3**: Vistas públicas con filtros
4. **Fase 4**: Dashboard vendedor
5. **Fase 5**: Productización (static files, email, etc.)