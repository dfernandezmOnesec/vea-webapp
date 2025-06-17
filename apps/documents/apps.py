from django.apps import AppConfig

class DocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.documents'

    def ready(self):
        print("DocumentsConfig ready: señales registradas")
        import apps.documents.signals 