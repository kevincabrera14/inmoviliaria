# Inmobiliaria Medellín

## 1. Concept & Vision

Plataforma inmobiliaria moderna para gestionar propiedades en los 10 municipios del Valle de Aburrá (Antioquia, Colombia). Sistema robusto con roles diferenciados: admins gestionan vendedores, vendedores publican propiedades, clientes navegan sin registro. Interfaz minimalista centrada en la ubicación geográfica, diseño mobile-first con colores azules profesionales.

## 2. Design System

### Colors
- **Primary**: #1e3a5f (Azul marino)
- **Primary Light**: #2a4a73
- **Secondary**: #4a90d9 (Azul claro)
- **Accent**: #64b5f6 (Azul brillante)
- **Background**: #ffffff
- **Surface**: #f8fafc
- **Text**: #1e293b
- **Text Muted**: #64748b
- **Border**: #e2e8f0
- **Success**: #10b981
- **Error**: #ef4444

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 400, 500, 600, 700

### Mobile-First Breakpoints
- Mobile: < 576px
- Tablet: 576px - 992px
- Desktop: > 992px

### CSS Architecture
- Custom CSS (sin framework)
- CSS Variables para theming
- Grid system propio
- Componentes reutilizables

## 3. Arquitectura

### Stack
- **Backend**: Django 5 + Django REST Framework
- **Base de datos**: PostgreSQL (Railway)
- **Almacenamiento imágenes**: WhiteNoise
- **Deployment**: Railway
- **CSS**: Custom (sin framework)

### Estructura de Apps
```
core/
├── users/           # Modelo User custom, auth, roles
├── properties/      # Modelo Property, imágenes, CRUD
├── locations/       # Modelo Municipality, Zone
└── core/            # Configuración principal, URLs, settings
```

## 4. Modelos

### User (extend Django AbstractUser)
- `role`: choices [admin, vendedor, cliente]
- `cedula`: string único (cédula colombiana)
- `telefono`: string opcional
- `is_active`: boolean

### Zone
- `name`: string (Zona Norte, Zona Centro, Zona Sur)
- `slug`: slug único
- `order`: int para ordenamiento

### Municipality
- `name`: string (10 municipios del Valle de Aburrá)
- **Zona Norte**: Barbosa, Girardota, Copacabana, Bello
- **Zona Centro**: Medellín
- **Zona Sur**: Envigado, Itagüí, Sabaneta, La Estrella, Caldas
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

## 5. Roles & Permisos

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

## 6. URLs

```
# Público
/                           # Landing con propiedades
/propiedades/              # Lista todas
/propiedades/<municipio>/  # Por municipio
/propiedad/<id>/          # Detalle

# Auth
/users/login/
/users/logout/

# Admin
/adminapp/                  # Django admin

# Dashboard
/dashboard/                # Panel principal
/dashboard/propiedades/    # Lista mis propiedades
/dashboard/propiedades/crear/
/dashboard/propiedades/<id>/editar/
/dashboard/propiedades/<id>/eliminar/
```

## 7. Templates

```
templates/
├── base.html              # Base con header/footer
├── home.html              # Landing page
├── properties/
│   ├── list.html          # Lista por municipio
│   └── detail.html        # Detalle propiedad
├── dashboard/
│   ├── base.html          # Dashboard base
│   └── vendor/
│       ├── dashboard.html
│       ├── property_list.html
│       └── property_form.html
├── users/
│   └── login.html
├── admin/
│   └── base.html          # Admin custom theme
└── partials/
    ├── header.html
    ├── footer.html
    └── property_card.html
```

## 8. Static Files

```
static/
├── css/
│   └── style.css          # Estilos custom mobile-first
└── admin/
    └── css/
        └── admin.css      # Theme admin
```

## 9. Variables de Entorno (.env)

```
DEBUG=False
SECRET_KEY=...
DATABASE_URL=postgres://...
ALLOWED_HOSTS=.railway.app
EMAIL_HOST=smtp.mailgun.org
EMAIL_FROM=info@inmobiliariamedellin.com
WHATSAPP_NUMBER=+573001234567
```

## 10. Deployment Railway

- `runtime.txt`: python-3.11
- `requirements.txt`: Django, gunicorn, whitenoise, psycopg2-binary, dj-database-url, python-dotenv
- `railway.json`: configuración de servicio
- `.gitignore`: excludes __pycache__, .env, *.pyc

## 11. Implementación

1. **Fase 1**: Modelos, admin Django, autenticación
2. **Fase 2**: CRUD propiedades con imágenes
3. **Fase 3**: Vistas públicas con filtros
4. **Fase 4**: Dashboard vendedor
5. **Fase 5**: Productización (static files, email, etc.)