from pathlib import Path
import os
import dj_database_url
import sys

# BASE_DIR apunta a la raíz del proyecto (vea-connect-website/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

if os.getenv("DJANGO_ENV") == "production":
    SECRET_KEY = os.environ["SECRET_KEY"]  # debe existir
else:
    SECRET_KEY = "dev-secret-key-unsafe"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Azure Function App Settings
FUNCTION_APP_URL = os.environ.get('FUNCTION_APP_URL') # ej: https://func-vea-connect-dev.azurewebsites.net/api/FunctionName
FUNCTION_APP_KEY = os.environ.get('FUNCTION_APP_KEY') # La clave 'default' de tus Host Keys

# -------------------------
# Base de Datos
# -------------------------
# Configuración de base de datos según el entorno
if os.getenv('CI_ENVIRONMENT') == 'true':
    # Entorno de CI/CD - PostgreSQL local
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
elif 'test' in sys.argv:
    # Modo de prueba - SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3_test',
        }
    }
else:
    # Desarrollo local y producción - usar dj_database_url
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith('sqlite'):
        # Si es SQLite, no usar parámetros de PostgreSQL
        DATABASES = {
            'default': dj_database_url.config(
                default=database_url,
                conn_max_age=600
            )
        }
    else:
        # Para PostgreSQL, incluir parámetros SSL
        DATABASES = {
            'default': dj_database_url.config(
                default=database_url,
                conn_max_age=600,
                ssl_require=True
            )
        }

# -------------------------
# Aplicaciones instaladas
# -------------------------
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'storages',
    'widget_tweaks',

    # Apps del proyecto
    'apps.core',
    'apps.dashboard',
    'apps.documents.apps.DocumentsConfig',
    'apps.events',
    'apps.directory',
    'apps.donations',
    'apps.user_settings',
]

# -------------------------
# Middleware
# -------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Soporte para archivos estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------
# Enrutamiento principal
# -------------------------
ROOT_URLCONF = 'config.urls'

# -------------------------
# Configuración de templates
# -------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Plantillas globales
        'APP_DIRS': True,                  # Habilita templates por app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------------
# WSGI
# -------------------------
WSGI_APPLICATION = 'config.wsgi.application'

# -------------------------
# Internacionalización
# -------------------------
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# -------------------------
# Archivos estáticos
# -------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# -------------------------
# Archivos multimedia
# -------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------
# Autenticación personalizada
# -------------------------
AUTH_USER_MODEL = 'core.CustomUser'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# -------------------------
# Llave primaria por defecto
# -------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
