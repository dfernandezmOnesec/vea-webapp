from django.db import models
from django.contrib.auth import get_user_model
from utilities.azureblobstorage import get_blob_service_client, generate_blob_sas
from django.conf import settings
from datetime import datetime, timedelta

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
        """Devuelve una URL SAS temporal para el archivo en Azure Blob Storage."""
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