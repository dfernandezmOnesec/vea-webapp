from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),

    # Incluimos core con namespace
    path('', include(('apps.core.urls', 'core'), namespace='core')),

    # Dashboard principal
    path("dashboard/", include(("apps.dashboard.urls", "dashboard"), namespace="dashboard")),

    # Aplicación de eventos
    path("events/", include(("apps.events.urls", "events"), namespace="events")),

    # Aplicación de donaciones
    path("donations/", include(("apps.donations.urls", "donations"), namespace="donations")),

    # Aplicación de documentos
    path("documents/", include(("apps.documents.urls", "documents"), namespace="documents")),

    # Aplicación de directorio
    path("directory/", include(("apps.directory.urls", "directory"), namespace="directory")),

    # Configuración de usuario
    path("settings/", include(("apps.user_settings.urls", "user_settings"), namespace="user_settings")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
