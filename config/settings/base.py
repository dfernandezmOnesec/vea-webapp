from pathlib import Path
import os
import dj_database_url

# BASE_DIR apunta a la raíz del proyecto (vea-connect-website/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

if os.getenv("DJANGO_ENV") == "production":
    SECRET_KEY = os.environ["SECRET_KEY"]  # debe existir
else:
    SECRET_KEY = "dev-secret-key-unsafe"



# -------------------------
# Base de Datos (PostgreSQL)
# -------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
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
