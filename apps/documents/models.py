from django.db import models
from django.contrib.auth import get_user_model

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

    class Meta:
        ordering = ["-date"]
        verbose_name = "Documento"
        verbose_name_plural = "Documentos" 