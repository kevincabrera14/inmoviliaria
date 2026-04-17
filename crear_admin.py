import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User

def create_admin():
    username = 'admin'
    email = 'admin@ejemplo.com'
    password = 'admin123' 

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superusuario '{username}' creado con éxito.")
    else:
        print(f"El usuario '{username}' ya existe.")

if __name__ == '__main__':
    create_admin()