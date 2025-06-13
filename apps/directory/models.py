# apps/directory/models.py

from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    role = models.CharField(max_length=100, verbose_name="Rol")
    ministry = models.CharField(max_length=150, verbose_name="Ministerio")
    contact = models.CharField(max_length=100, verbose_name="Contacto")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ['name']
