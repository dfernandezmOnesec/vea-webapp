import os
from django.core.asgi import get_asgi_application

# Nombre real del paquete de configuración
PROJECT_PACKAGE = "config"

# Configuración para Azure App Service
if "WEBSITE_HOSTNAME" in os.environ:
    # Entorno de producción en Azure
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{PROJECT_PACKAGE}.settings.production")

    # Configurar Azure Monitor si está disponible
    try:
        from azure.monitor.opentelemetry import configure_azure_monitor
        from opentelemetry.instrumentation.django import DjangoInstrumentor

        if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
            configure_azure_monitor(
                connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
            )
            DjangoInstrumentor().instrument()
    except ImportError:
        print("ℹAzure Monitor no está configurado (paquetes no instalados)")
else:
    # Entorno local (dev)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{PROJECT_PACKAGE}.settings.development")
    print("⚙️ Modo desarrollo activado - ASGI")

# Obtener la aplicación ASGI
application = get_asgi_application()
