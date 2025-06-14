import os
from dotenv import load_dotenv
from .base import *
import dj_database_url
import urllib.parse

# Cargar variables de entorno desde el archivo .env (solo en desarrollo local)
load_dotenv()

# Variables específicas de Azure Blob Storage
BLOB_ACCOUNT_NAME = os.getenv('BLOB_ACCOUNT_NAME')
BLOB_ACCOUNT_KEY = os.getenv('BLOB_ACCOUNT_KEY')
BLOB_CONTAINER_NAME = os.getenv('BLOB_CONTAINER_NAME')

# Debug settings
DEBUG = True

# Base de datos PostgreSQL para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vea_connect',
        'USER': 'twsugyiaxf',
        'PASSWORD': 'E72$rhqEdm6b9oaI',
        'HOST': 'micrositio-vea-connect-server.postgres.database.azure.com',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require'
        }
    }
}

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Seguridad para entorno local
SECRET_KEY = 'django-insecure-+p^1$!j%r!@$%^&*(devkeyhere'
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
