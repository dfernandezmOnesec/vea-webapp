from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Donation, DonationType

class DonationForm(forms.ModelForm):
    donation_type = forms.ModelChoiceField(
        queryset=DonationType.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'required': True}),
        label=_('Tipo de donación')
    )

    class Meta:
        model = Donation
        fields = [
            'title',
            'donation_type',
            'amount',
            'description',
            'method',
            'entity',
            'bank',
            'clabe',
            'location'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'method': forms.Select(attrs={'class': 'form-select'}),
            'entity': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'clabe': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'title': _('Título'),
            'amount': _('Monto'),
            'description': _('Descripción'),
            'method': _('Método de pago'),
            'entity': _('Entidad'),
            'bank': _('Banco'),
            'clabe': _('CLABE'),
            'location': _('Ubicación')
        }

    def clean(self):
        cleaned_data = super().clean()
        donation_type = cleaned_data.get('donation_type')
        amount = cleaned_data.get('amount')

        if donation_type and donation_type.name == 'Monetaria' and not amount:
            raise forms.ValidationError(_('El monto es requerido para donaciones monetarias'))

        return cleaned_data
        