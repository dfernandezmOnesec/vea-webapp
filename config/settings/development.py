import os
from dotenv import load_dotenv
from .base import *

# Cargar variables de entorno desde el archivo .env (solo en desarrollo local)
load_dotenv()

# Configuración de base de datos
if os.getenv('CI_ENVIRONMENT') == 'true':
    # Configuración para CI/CD
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DBNAME', 'postgres'),
            'USER': os.environ.get('DBUSER', 'postgres'),
            'PASSWORD': os.environ.get('DBPASS', 'postgres'),
            'HOST': os.environ.get('DBHOST', 'localhost'),
            'PORT': os.environ.get('DBPORT', '5432'),
        }
    }
else:
    # Configuración para desarrollo local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Variables específicas de Azure Blob Storage (opcionales en desarrollo)
BLOB_ACCOUNT_NAME = os.getenv('BLOB_ACCOUNT_NAME')
BLOB_ACCOUNT_KEY = os.getenv('BLOB_ACCOUNT_KEY')
BLOB_CONTAINER_NAME = os.getenv('BLOB_CONTAINER_NAME')

# Validación de variables de entorno
if not all([BLOB_ACCOUNT_NAME, BLOB_ACCOUNT_KEY, BLOB_CONTAINER_NAME]):
    raise ValueError("""
    Faltan variables de entorno necesarias para Azure Blob Storage.
    Por favor, asegúrate de tener definidas:
    - BLOB_ACCOUNT_NAME
    - BLOB_ACCOUNT_KEY
    - BLOB_CONTAINER_NAME
    """)

# Debug settings
DEBUG = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Seguridad para entorno local
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-+p^1$!j%r!@$%^&*(devkeyhere')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Redis opcional (si se desea usar Redis Cloud también en desarrollo)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Sesiones en caché (opcional)
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Configuración de Azure Blob Storage (solo si las variables están disponibles)
if all([BLOB_ACCOUNT_NAME, BLOB_ACCOUNT_KEY, BLOB_CONTAINER_NAME]):
    AZURE_STORAGE_CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={BLOB_ACCOUNT_NAME};AccountKey={BLOB_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
else:
    # Usar almacenamiento local si no hay configuración de Azure
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
