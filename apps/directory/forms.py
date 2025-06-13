# apps/directory/forms.py

from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'role', 'ministry', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el rol'}),
            'ministry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el ministerio'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el contacto'}),
        }
