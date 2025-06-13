from django.db import models
from django.contrib.auth import get_user_model

class Document(models.Model):
    CATEGORY_CHOICES = [
        ("eventos_generales", "Eventos generales"),
        ("ministerios", "Ministerios"),
        ("formacion", "Formación"),
        ("campanas", "Campañas"),
    ]

    title = models.CharField("Título", max_length=255)
    file = models.FileField("Archivo", upload_to="documents/")
    description = models.TextField("Descripción", blank=True)
    category = models.CharField("Categoría", max_length=32, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField("Fecha de subida", auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), verbose_name="Propietario", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Documento"
        verbose_name_plural = "Documentos" 