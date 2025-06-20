import os
from .base import *

# Configuración de producción para Azure
DEBUG = False

# Configuración de seguridad
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuración de base de datos para producción
# Usar DATABASE_URL desde Azure Key Vault
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Configuración de Azure Blob Storage para producción
AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
BLOB_ACCOUNT_NAME = os.environ.get('BLOB_ACCOUNT_NAME')
BLOB_ACCOUNT_KEY = os.environ.get('BLOB_ACCOUNT_KEY')
BLOB_CONTAINER_NAME = os.environ.get('BLOB_CONTAINER_NAME')

# Configuración de archivos estáticos para Azure
STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = BLOB_ACCOUNT_NAME
AZURE_ACCOUNT_KEY = BLOB_ACCOUNT_KEY
AZURE_CUSTOM_DOMAIN = f'{BLOB_ACCOUNT_NAME}.blob.core.windows.net'
AZURE_STATIC_CONTAINER = 'static'

# Configuración de archivos multimedia para Azure
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_MEDIA_CONTAINER = 'media'

# Configuración de caché para Azure Redis (opcional)
# Temporarily disabled until django-redis is installed
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Configuración de sesiones
# Temporarily using database sessions instead of cache
SESSION_ENGINE = "django.contrib.sessions.backends.db"
# SESSION_CACHE_ALIAS = "default"

# Configuración de logging para Azure
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# No usar dotenv en producción

ALLOWED_HOSTS = [os.environ.get('WEBSITE_HOSTNAME', '127.0.0.1'), 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE[1:]

# Archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Construcción explícita del Redis URL desde las variables individuales
# Temporarily disabled until django-redis is installed
# REDIS_USERNAME = os.getenv("REDIS_USERNAME")
# REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
# REDIS_HOST = os.getenv("REDIS_HOST")
# REDIS_PORT = os.getenv("REDIS_PORT")

# REDIS_URL = f"rediss://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

# Sesiones
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"