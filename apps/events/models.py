# apps/events/models.py

from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título del evento")
    description = models.TextField(blank=True, verbose_name="Descripción")
    date = models.DateField(verbose_name="Fecha")
    time = models.TimeField(verbose_name="Hora")
    location = models.CharField(max_length=255, verbose_name="Lugar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.title} - {self.date}"
