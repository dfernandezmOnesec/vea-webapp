from django.apps import AppConfig

class DirectoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.directory'

    def ready(self):
        import apps.directory.signals 