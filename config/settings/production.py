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
db_name = os.environ.get('AZURE_POSTGRESQL_NAME')
db_user = os.environ.get('AZURE_POSTGRESQL_USERNAME')
db_password = os.environ.get('AZURE_POSTGRESQL_PASSWORD')
db_host = os.environ.get('AZURE_POSTGRESQL_HOST')
db_port = os.environ.get('DB_PORT', '5432')

# --- TEMPORARY DEBUGGING ---
print(f"DEBUG DB_NAME: {db_name}")
print(f"DEBUG DB_USER: {db_user}")
print(f"DEBUG DB_HOST: {db_host}")
print(f"DEBUG DB_PORT: {db_port}")
print(f"DEBUG DB_PASSWORD IS SET: {'Yes' if db_password else 'No'}")
# --- END TEMPORARY DEBUGGING ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
        'PORT': db_port,
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

ALLOWED_HOSTS = [
    os.environ.get('WEBSITE_HOSTNAME', '127.0.0.1'), 
    'localhost', 
    '127.0.0.1',
    '169.254.130.4',  # IP interna de Azure
    '169.254.0.0/16',  # Rango de IPs internas de Azure
    '*',  # Temporalmente permitir todos los hosts para debugging
]

# Configurar CSRF_TRUSTED_ORIGINS de manera segura
website_hostname = os.environ.get('WEBSITE_HOSTNAME')
if website_hostname:
    CSRF_TRUSTED_ORIGINS = [f'https://{website_hostname}']
else:
    # Fallback para desarrollo o cuando WEBSITE_HOSTNAME no está configurado
    CSRF_TRUSTED_ORIGINS = ['https://localhost', 'https://127.0.0.1']

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

MEDIA_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{AZURE_MEDIA_CONTAINER}/"