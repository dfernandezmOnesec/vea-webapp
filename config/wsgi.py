"""
WSGI config for vea_connect project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see:
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# ✅ Nombre real del paquete que contiene settings
PROJECT_PACKAGE = "config"

# Configuración de entorno
if "WEBSITE_HOSTNAME" in os.environ:
    # Entorno de producción en Azure
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{PROJECT_PACKAGE}.settings.production")

    # Configuración de Azure Monitor (Application Insights)
    if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        try:
            from azure.monitor.opentelemetry import configure_azure_monitor
            from opentelemetry.instrumentation.django import DjangoInstrumentor

            configure_azure_monitor(
                connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
            )
            DjangoInstrumentor().instrument()
            print("Azure Monitor configurado correctamente para WSGI")
        except ImportError:
            print("⚠️ Paquetes de Azure Monitor no instalados. Ejecuta:")
            print("pip install azure-monitor-opentelemetry opentelemetry-instrumentation-django")
else:
    # Entorno de desarrollo local
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{PROJECT_PACKAGE}.settings.development")
    print("⚙️ Modo desarrollo activado - WSGI")

# Obtener la aplicación WSGI
application = get_wsgi_application()
