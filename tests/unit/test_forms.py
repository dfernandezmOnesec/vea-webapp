"""
Pruebas unitarias para formularios
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal

from apps.core.models import CustomUser
from apps.directory.forms import ContactForm
from apps.documents.forms import DocumentForm
from apps.events.forms import EventForm
from apps.donations.forms import DonationForm
from apps.donations.models import DonationType


class ContactFormTest(TestCase):
    """Pruebas para el formulario ContactForm"""

    def test_contact_form_valid(self):
        """Prueba que el formulario sea válido con datos correctos"""
        form_data = {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'role': 'Pastor',
            'ministry': 'Ministerio de Jóvenes',
            'contact': 'juan@iglesia.com'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_missing_required(self):
        """Prueba que el formulario sea inválido sin campos requeridos"""
        form_data = {
            'first_name': 'Juan',
            # Falta last_name, ministry y contact
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertIn('ministry', form.errors)
        self.assertIn('contact', form.errors)

    def test_contact_form_save(self):
        """Prueba que el formulario guarde correctamente"""
        form_data = {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'role': 'Pastor',
            'ministry': 'Ministerio de Jóvenes',
            'contact': 'juan@iglesia.com'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
        contact = form.save()
        self.assertEqual(contact.first_name, 'Juan')
        self.assertEqual(contact.last_name, 'Pérez')
        self.assertEqual(contact.role, 'Pastor')
        self.assertEqual(contact.ministry, 'Ministerio de Jóvenes')
        self.assertEqual(contact.contact, 'juan@iglesia.com')


class DocumentFormTest(TestCase):
    """Pruebas para el formulario DocumentForm"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser'
        )

    def test_document_form_valid(self):
        """Prueba que el formulario sea válido con datos correctos"""
        # Crear un archivo de prueba
        test_file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        form_data = {
            'title': 'Documento de prueba',
            'description': 'Descripción de prueba',
            'category': 'eventos_generales'
        }
        form_files = {
            'file': test_file
        }
        form = DocumentForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())

    def test_document_form_invalid_missing_required(self):
        """Prueba que el formulario sea inválido sin campos requeridos"""
        form_data = {
            'description': 'Descripción de prueba',
            # Falta title, file y category
        }
        form = DocumentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('file', form.errors)
        self.assertIn('category', form.errors)

    def test_document_form_category_choices(self):
        """Prueba las opciones de categoría válidas"""
        test_file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        valid_categories = [
            "eventos_generales",
            "ministerios",
            "formacion",
            "campanas",
            "avisos_globales"
        ]
        
        for category in valid_categories:
            form_data = {
                'title': f'Documento {category}',
                'category': category
            }
            form_files = {
                'file': test_file
            }
            form = DocumentForm(data=form_data, files=form_files)
            self.assertTrue(form.is_valid(), f"Formulario inválido para categoría: {category}")

    def test_document_form_save(self):
        """Prueba que el formulario guarde correctamente"""
        test_file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        form_data = {
            'title': 'Documento de prueba',
            'description': 'Descripción de prueba',
            'category': 'eventos_generales'
        }
        form_files = {
            'file': test_file
        }
        form = DocumentForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())
        document = form.save(commit=False)
        document.user = self.user
        document.save()
        self.assertEqual(document.title, 'Documento de prueba')
        self.assertEqual(document.description, 'Descripción de prueba')
        self.assertEqual(document.category, 'eventos_generales')
        self.assertEqual(document.user, self.user)


class EventFormTest(TestCase):
    """Pruebas para el formulario EventForm"""

    def test_event_form_valid(self):
        """Prueba que el formulario sea válido con datos correctos"""
        form_data = {
            'title': 'Evento de prueba',
            'description': 'Descripción del evento',
            'date': '2024-12-25',
            'time': '18:00:00',
            'location': 'Iglesia Principal'
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_event_form_invalid_missing_required(self):
        """Prueba que el formulario sea inválido sin campos requeridos"""
        form_data = {
            'description': 'Descripción del evento',
            # Falta title
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_event_form_save(self):
        """Prueba que el formulario guarde correctamente"""
        form_data = {
            'title': 'Evento de prueba',
            'description': 'Descripción del evento',
            'date': '2024-12-25',
            'time': '18:00:00',
            'location': 'Iglesia Principal'
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())
        event = form.save()
        self.assertEqual(event.title, 'Evento de prueba')
        self.assertEqual(event.description, 'Descripción del evento')
        self.assertEqual(str(event.date), '2024-12-25')
        self.assertEqual(str(event.time), '18:00:00')
        self.assertEqual(event.location, 'Iglesia Principal')


class DonationFormTest(TestCase):
    """Pruebas para el formulario DonationForm"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser'
        )
        self.donation_type = DonationType.objects.create(name="Monetaria")

    def test_donation_form_valid(self):
        """Prueba que el formulario sea válido con datos correctos"""
        form_data = {
            'title': 'Donación de prueba',
            'donation_type': self.donation_type.id,
            'amount': '100.00',
            'description': 'Descripción de la donación',
            'method': 'deposito',
            'entity': 'Banco de México',
            'bank': 'Banamex',
            'clabe': '012345678901234567',
            'location': 'Sucursal Centro'
        }
        form = DonationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_donation_form_invalid_missing_required(self):
        """Prueba que el formulario sea inválido sin campos requeridos"""
        form_data = {
            'description': 'Descripción de la donación',
            # Falta title y donation_type
        }
        form = DonationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('donation_type', form.errors)

    def test_donation_form_method_choices(self):
        """Prueba las opciones de método válidas"""
        valid_methods = [
            'deposito',
            'transferencia',
            'relaciones_publicas',
            'ministerio',
            'entrega_directa'
        ]
        
        for method in valid_methods:
            form_data = {
                'title': f'Donación {method}',
                'donation_type': self.donation_type.id,
                'method': method
            }
            form = DonationForm(data=form_data)
            self.assertTrue(form.is_valid(), f"Formulario inválido para método: {method}")

    def test_donation_form_save(self):
        """Prueba que el formulario guarde correctamente"""
        form_data = {
            'title': 'Donación de prueba',
            'donation_type': self.donation_type.id,
            'amount': '100.00',
            'description': 'Descripción de la donación',
            'method': 'deposito',
            'entity': 'Banco de México'
        }
        form = DonationForm(data=form_data)
        self.assertTrue(form.is_valid())
        donation = form.save(commit=False)
        donation.created_by = self.user
        donation.save()
        self.assertEqual(donation.title, 'Donación de prueba')
        self.assertEqual(donation.donation_type, self.donation_type)
        self.assertEqual(donation.amount, Decimal('100.00'))
        self.assertEqual(donation.description, 'Descripción de la donación')
        self.assertEqual(donation.method, 'deposito')
        self.assertEqual(donation.entity, 'Banco de México')
        self.assertEqual(donation.created_by, self.user) 