import os
from .base import *

SECRET_KEY = os.environ.get("SECRET_KEY")


# No usar dotenv en producción

ALLOWED_HOSTS = [os.environ.get('WEBSITE_HOSTNAME', '127.0.0.1'), 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
DEBUG = True


# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE[1:]

# Archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['AZURE_POSTGRESQL_DATABASE'],
        'HOST': os.environ['AZURE_POSTGRESQL_HOST'],
        'USER': os.environ['AZURE_POSTGRESQL_USERNAME'],
        'PASSWORD': os.environ['AZURE_POSTGRESQL_PASSWORD'],
    }
}

# Construcción explícita del Redis URL desde las variables individuales
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

REDIS_URL = f"rediss://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


# Azure Blob Storage
BLOB_ACCOUNT_NAME = os.environ.get('BLOB_ACCOUNT_NAME')
BLOB_ACCOUNT_KEY = os.environ.get('BLOB_ACCOUNT_KEY')
BLOB_CONTAINER_NAME = os.environ.get('BLOB_CONTAINER_NAME')

# Sesiones
SESSION_ENGINE = "django.contrib.sessions.backends.cache"