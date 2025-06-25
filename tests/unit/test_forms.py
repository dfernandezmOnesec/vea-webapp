"""
Pruebas unitarias para formularios
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal


class ContactFormTest(TestCase):
    """Pruebas para el formulario ContactForm"""

    def test_contact_form_valid(self):
        """Prueba que el formulario sea válido con datos correctos"""
        from apps.directory.forms import ContactForm
        form_data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'role': 'Pastor',
            'ministry': 'Ministerio de Jovenes',
            'contact': 'juan@iglesia.com'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_missing_required(self):
        """Prueba que el formulario sea inválido sin campos requeridos"""
        from apps.directory.forms import ContactForm
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
        from apps.directory.forms import ContactForm
        form_data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'role': 'Pastor',
            'ministry': 'Ministerio de Jovenes',
            'contact': 'juan@iglesia.com'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
        contact = form.save()
        self.assertEqual(contact.first_name, 'Juan')
        self.assertEqual(contact.last_name, 'Perez')
        self.assertEqual(contact.role, 'Pastor')
        self.assertEqual(contact.ministry, 'Ministerio de Jovenes')
        self.assertEqual(contact.contact, 'juan@iglesia.com')


class DocumentFormTest(TestCase):
    """Pruebas para el formulario DocumentForm"""

    def setUp(self):
        from apps.core.models import CustomUser
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser'
        )

    def test_document_form_valid(self):
        """Prueba que el formulario sea válido con datos correctos"""
        from apps.documents.forms import DocumentForm
        # Crear un archivo de prueba
        test_file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        form_data = {
            'title': 'Documento de prueba',
            'description': 'Descripcion de prueba',
            'category': 'eventos_generales'
        }
        form_files = {
            'file': test_file
        }
        form = DocumentForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())

    def test_document_form_invalid_missing_required(self):
        """Prueba que el formulario sea inválido sin campos requeridos"""
        from apps.documents.forms import DocumentForm
        form_data = {
            'description': 'Descripcion de prueba',
            # Falta title, file y category
        }
        form = DocumentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('file', form.errors)
        self.assertIn('category', form.errors)

    def test_document_form_category_choices(self):
        """Prueba las opciones de categoría válidas"""
        from apps.documents.forms import DocumentForm
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
            self.assertTrue(form.is_valid(), f"Formulario invalido para categoria: {category}")

    def test_document_form_save(self):
        """Prueba que el formulario guarde correctamente"""
        from apps.documents.forms import DocumentForm
        test_file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        form_data = {
            'title': 'Documento de prueba',
            'description': 'Descripcion de prueba',
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
        self.assertEqual(document.description, 'Descripcion de prueba')
        self.assertEqual(document.category, 'eventos_generales')
        self.assertEqual(document.user, self.user)


class EventFormTest(TestCase):
    """Pruebas para el formulario EventForm"""

    def test_event_form_valid(self):
        """Prueba que el formulario sea válido con datos correctos"""
        from apps.events.forms import EventForm
        form_data = {
            'title': 'Evento de prueba',
            'description': 'Descripcion del evento',
            'date': '2024-12-25',
            'time': '18:00:00',
            'location': 'Iglesia Principal'
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_event_form_invalid_missing_required(self):
        """Prueba que el formulario sea inválido sin campos requeridos"""
        from apps.events.forms import EventForm
        form_data = {
            'description': 'Descripcion del evento',
            # Falta title
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_event_form_save(self):
        """Prueba que el formulario guarde correctamente"""
        from apps.events.forms import EventForm
        form_data = {
            'title': 'Evento de prueba',
            'description': 'Descripcion del evento',
            'date': '2024-12-25',
            'time': '18:00:00',
            'location': 'Iglesia Principal'
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())
        event = form.save()
        self.assertEqual(event.title, 'Evento de prueba')
        self.assertEqual(event.description, 'Descripcion del evento')
        self.assertEqual(str(event.date), '2024-12-25')
        self.assertEqual(str(event.time), '18:00:00')
        self.assertEqual(event.location, 'Iglesia Principal')


class DonationFormTest(TestCase):
    """Pruebas para el formulario DonationForm"""

    def setUp(self):
        from apps.core.models import CustomUser
        from apps.donations.models import DonationType
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser'
        )
        self.donation_type = DonationType.objects.create(name="Monetaria")

    def test_donation_form_valid(self):
        """Prueba que el formulario sea válido con datos correctos"""
        from apps.donations.forms import DonationForm
        form_data = {
            'title': 'Donacion de prueba',
            'donation_type': self.donation_type.id,
            'amount': '100.00',
            'description': 'Descripcion de la donacion',
            'method': 'deposito',
            'entity': 'Banco de Mexico',
            'bank': 'Banamex',
            'clabe': '012345678901234567',
            'location': 'Sucursal Centro'
        }
        form = DonationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_donation_form_invalid_missing_required(self):
        """Prueba que el formulario sea inválido sin campos requeridos"""
        from apps.donations.forms import DonationForm
        form_data = {
            'description': 'Descripcion de la donacion',
            # Falta title y donation_type
        }
        form = DonationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('donation_type', form.errors)

    def test_donation_form_method_choices(self):
        """Prueba las opciones de método válidas"""
        from apps.donations.forms import DonationForm
        valid_methods = [
            'deposito',
            'transferencia',
            'relaciones_publicas',
            'ministerio',
            'entrega_directa'
        ]
        
        for method in valid_methods:
            form_data = {
                'title': f'Donacion {method}',
                'donation_type': self.donation_type.id,
                'method': method
            }
            form = DonationForm(data=form_data)
            self.assertTrue(form.is_valid(), f"Formulario invalido para metodo: {method}")

    def test_donation_form_save(self):
        """Prueba que el formulario guarde correctamente"""
        from apps.donations.forms import DonationForm
        form_data = {
            'title': 'Donacion de prueba',
            'donation_type': self.donation_type.id,
            'amount': '100.00',
            'description': 'Descripcion de la donacion',
            'method': 'deposito',
            'entity': 'Banco de Mexico'
        }
        form = DonationForm(data=form_data)
        self.assertTrue(form.is_valid())
        donation = form.save(commit=False)
        donation.created_by = self.user
        donation.save()
        self.assertEqual(donation.title, 'Donacion de prueba')
        self.assertEqual(donation.donation_type, self.donation_type)
        self.assertEqual(donation.amount, Decimal('100.00'))
        self.assertEqual(donation.description, 'Descripcion de la donacion')
        self.assertEqual(donation.method, 'deposito')
        self.assertEqual(donation.entity, 'Banco de Mexico')
        self.assertEqual(donation.created_by, self.user) 