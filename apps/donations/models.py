from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError



class DonationType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Nombre del tipo de donación'))
    def __str__(self):
        return self.name


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
        verbose_name=_('Título')
    )
    donation_type = models.ForeignKey(
        'DonationType',
        on_delete=models.PROTECT,
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
        blank=True,
        verbose_name=_('Creado por')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de creación')
    )

    class Meta:
        verbose_name = _('Donación')
        verbose_name_plural = _('Donaciones')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title or self.get_donation_type_display()} - {self.created_at.strftime('%d/%m/%Y')}"
    
    def clean(self):
        # Solo validar monto negativo si el tipo es Monetaria
        if self.donation_type and self.donation_type.name.lower() == "monetaria":
            if self.amount is not None and self.amount < 0:
                raise ValidationError("El valor de la donación monetaria no puede ser negativo.")
    
    def save(self, *args, **kwargs):
        """Validar antes de guardar"""
        self.full_clean()
        super().save(*args, **kwargs)
        