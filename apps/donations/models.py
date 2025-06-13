from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class Donation(models.Model):
    TYPE_CHOICES = [
        ('monetaria', _('Monetaria')),
        ('especie', _('En especie')),
        ('medicamentos', _('Medicamentos')),
        ('voluntariado', _('Voluntariado')),
        ('otros', _('Otros')),
    ]

    METHOD_CHOICES = [
        ('deposito', 'Depósito bancario'),
        ('transferencia', 'Transferencia electrónica'),
        ('relaciones_publicas', 'Mesa de Relaciones Públicas'),
        ('ministerio', 'Encargado de Ministerio'),
        ('entrega_directa', 'Entrega directa en instalaciones'),
    ]

    title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('Título')
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name=_('Tipo de donación')
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Monto')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Descripción')
    )
    method = models.CharField(
        max_length=100,
        choices=METHOD_CHOICES,
        blank=True,
        null=True,
        verbose_name=_('Método de pago')
    )
    entity = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Entidad')
    )
    bank = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Banco')
    )
    number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('Número de cuenta')
    )
    clabe = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('CLABE')
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('Ubicación')
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Creado por')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de creación')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Fecha de actualización')
    )

    class Meta:
        verbose_name = _('Donación')
        verbose_name_plural = _('Donaciones')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title or self.get_type_display()} - {self.created_at.strftime('%d/%m/%Y')}"
        