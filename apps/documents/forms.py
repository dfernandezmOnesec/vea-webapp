# apps/documents/forms.py

from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "file", "description", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título del documento"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".pdf,.jpg,.jpeg,.png,.docx,.pptx"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripción", "rows": 2}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
