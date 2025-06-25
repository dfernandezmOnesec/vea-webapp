from django.db import models
from django.contrib.auth import get_user_model
from utilities.azureblobstorage import get_blob_service_client, generate_blob_sas
from django.conf import settings
from datetime import datetime, timedelta
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Document(models.Model):
    CATEGORY_CHOICES = [
        ("eventos_generales", "Eventos generales"),
        ("ministerios", "Ministerios"),
        ("formacion", "Formación"),
        ("campanas", "Campañas"),
        ("avisos_globales", "Avisos globales"),
    ]

    title = models.CharField("Título", max_length=255)
    file = models.FileField("Archivo", upload_to="documents/")
    description = models.TextField("Descripción", blank=True)
    category = models.CharField("Categoría", max_length=32, choices=CATEGORY_CHOICES)
    date = models.DateTimeField("Fecha", blank=True, null=True)
    user = models.ForeignKey(get_user_model(), verbose_name="Usuario", on_delete=models.CASCADE, db_column="user_id", blank=True, null=True)
    file_type = models.CharField("Tipo de archivo", max_length=32, blank=True, null=True)
    is_processed = models.BooleanField("¿Procesado?", default=False)
    processing_status = models.CharField("Estado de procesamiento", max_length=32, default="pendiente")
    metadata = models.JSONField("Metadatos", default=dict, blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def sas_url(self):
        """Devuelve una URL SAS temporal para el archivo en Azure Blob Storage (sin verificar existencia)."""
        if not self.file:
            return None
        account_name = settings.BLOB_ACCOUNT_NAME
        account_key = settings.BLOB_ACCOUNT_KEY
        container_name = settings.BLOB_CONTAINER_NAME
        blob_name = self.file.name
        try:
            from azure.storage.blob import generate_blob_sas, BlobSasPermissions
            sas_token = generate_blob_sas(
                account_name=account_name,
                container_name=container_name,
                blob_name=blob_name,
                account_key=account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=2)
            )
            return f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
        except Exception as e:
            return None

    class Meta:
        ordering = ["-date"]
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

# Señal para eliminar el blob de Azure cuando se elimina un documento
@receiver(post_delete, sender=Document)
def delete_blob_on_document_delete(sender, instance, **kwargs):
    if instance.file:
        try:
            from utilities.azureblobstorage import get_blob_service_client
            blob_service_client = get_blob_service_client()
            container_client = blob_service_client.get_container_client(settings.BLOB_CONTAINER_NAME)
            blob_client = container_client.get_blob_client(instance.file.name)
            if blob_client.exists():
                blob_client.delete_blob()
                print(f"Blob eliminado: {instance.file.name}")
        except Exception as e:
            print(f"Error eliminando blob: {e}") 