from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            'title',
            'type',
            'amount',
            'description',
            'method',
            'entity',
            'bank',
            'number',
            'clabe',
            'location'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'type': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'method': forms.Select(attrs={'class': 'form-select'}),
            'entity': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'clabe': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'title': _('Título'),
            'type': _('Tipo de donación'),
            'amount': _('Monto'),
            'description': _('Descripción'),
            'method': _('Método de pago'),
            'entity': _('Entidad'),
            'bank': _('Banco'),
            'number': _('Número de cuenta'),
            'clabe': _('CLABE'),
            'location': _('Ubicación')
        }

    def clean(self):
        cleaned_data = super().clean()
        donation_type = cleaned_data.get('type')
        amount = cleaned_data.get('amount')

        if donation_type == 'monetaria' and not amount:
            raise forms.ValidationError(_('El monto es requerido para donaciones monetarias'))

        return cleaned_data
        