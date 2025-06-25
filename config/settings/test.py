import os
from .base import *

# Configuración específica para pruebas
DEBUG = False

# Configuración de base de datos para pruebas
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3_test',
        'OPTIONS': {
            'timeout': 20,
        }
    }
}

# Configuración de caché para pruebas
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Configuración de sesiones para pruebas
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Configuración de archivos estáticos para pruebas
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_test'

# Configuración de archivos multimedia para pruebas
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media_test'

# Configuración de seguridad para pruebas
SECRET_KEY = 'test-secret-key-for-testing-only'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

# Configuración de logging para pruebas
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Configuración de archivos para pruebas
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Configuración de correo para pruebas
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Configuración de timezone para pruebas
USE_TZ = False
TIME_ZONE = 'UTC'

# Configuración de Azure Blob Storage para pruebas (deshabilitado)
BLOB_ACCOUNT_NAME = None
BLOB_ACCOUNT_KEY = None
BLOB_CONTAINER_NAME = None
AZURE_STORAGE_CONNECTION_STRING = None

# Configuración para deshabilitar signals de Azure durante pruebas
DISABLE_AZURE_SIGNALS = True 