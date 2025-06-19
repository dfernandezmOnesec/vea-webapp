#!/bin/bash

# Migrar base de datos
python manage.py migrate

# Recoger archivos estáticos
python manage.py collectstatic --noinput

# Iniciar Gunicorn
gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 4