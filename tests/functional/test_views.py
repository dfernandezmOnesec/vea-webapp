"""
Pruebas funcionales para las vistas de la aplicación
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal

from apps.core.models import CustomUser
from apps.directory.models import Contact
from apps.documents.models import Document
from apps.events.models import Event
from apps.donations.models import Donation, DonationType

User = get_user_model()


class CoreViewsTest(TestCase):
    """Pruebas para las vistas del core"""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_index_view(self):
        """Prueba la vista principal"""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_base_template(self):
        """Prueba que el template base funcione"""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'VEA WebApp')


class DirectoryViewsTest(TestCase):
    """Pruebas para las vistas del directorio"""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.contact = Contact.objects.create(
            name="Juan Pérez",
            role="Pastor",
            ministry="Ministerio de Jóvenes",
            contact="juan@iglesia.com"
        )

    def test_contact_list_view(self):
        """Prueba la vista de lista de contactos"""
        response = self.client.get(reverse('directory:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'directory/directory.html')
        self.assertContains(response, "Juan Pérez")

    def test_contact_create_view_get(self):
        """Prueba la vista de creación de contacto (GET)"""
        response = self.client.get(reverse('directory:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'directory/create.html')

    def test_contact_create_view_post(self):
        """Prueba la vista de creación de contacto (POST)"""
        data = {
            'name': 'Ana García',
            'role': 'Líder',
            'ministry': 'Ministerio de Mujeres',
            'contact': 'ana@iglesia.com'
        }
        response = self.client.post(reverse('directory:create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Contact.objects.filter(name='Ana García').exists())

    def test_contact_edit_view_get(self):
        """Prueba la vista de edición de contacto (GET)"""
        response = self.client.get(reverse('directory:edit', args=[self.contact.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'directory/create.html')
        self.assertContains(response, "Juan Pérez")

    def test_contact_edit_view_post(self):
        """Prueba la vista de edición de contacto (POST)"""
        data = {
            'name': 'Juan Pérez Actualizado',
            'role': 'Pastor Principal',
            'ministry': 'Ministerio de Jóvenes',
            'contact': 'juan@iglesia.com'
        }
        response = self.client.post(reverse('directory:edit', args=[self.contact.pk]), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, 'Juan Pérez Actualizado')

    def test_contact_delete_view_get(self):
        """Prueba la vista de eliminación de contacto (GET)"""
        response = self.client.get(reverse('directory:delete', args=[self.contact.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'directory/delete.html')

    def test_contact_delete_view_post(self):
        """Prueba la vista de eliminación de contacto (POST)"""
        response = self.client.post(reverse('directory:delete', args=[self.contact.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())


class DocumentsViewsTest(TestCase):
    """Pruebas para las vistas de documentos"""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.document = Document.objects.create(
            title="Documento de prueba",
            description="Descripción de prueba",
            category="eventos_generales",
            user=self.user
        )

    def test_document_list_view(self):
        """Prueba la vista de lista de documentos"""
        response = self.client.get(reverse('documents:document_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/documents.html')
        self.assertContains(response, "Documento de prueba")

    def test_document_create_view_get(self):
        """Prueba la vista de creación de documento (GET)"""
        response = self.client.get(reverse('documents:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/create.html')

    def test_document_create_view_post(self):
        """Prueba la vista de creación de documento (POST)"""
        test_file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        data = {
            'title': 'Nuevo documento',
            'description': 'Descripción del nuevo documento',
            'category': 'ministerios'
        }
        files = {
            'file': test_file
        }
        response = self.client.post(reverse('documents:create'), data, files=files)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Document.objects.filter(title='Nuevo documento').exists())

    def test_document_edit_view_get(self):
        """Prueba la vista de edición de documento (GET)"""
        response = self.client.get(reverse('documents:edit', args=[self.document.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/create.html')
        self.assertContains(response, "Documento de prueba")

    def test_document_edit_view_post(self):
        """Prueba la vista de edición de documento (POST)"""
        data = {
            'title': 'Documento actualizado',
            'description': 'Descripción actualizada',
            'category': 'formacion'
        }
        response = self.client.post(reverse('documents:edit', args=[self.document.pk]), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.document.refresh_from_db()
        self.assertEqual(self.document.title, 'Documento actualizado')

    def test_document_delete_view_get(self):
        """Prueba la vista de eliminación de documento (GET)"""
        response = self.client.get(reverse('documents:delete', args=[self.document.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/confirm_delete.html')

    def test_document_delete_view_post(self):
        """Prueba la vista de eliminación de documento (POST)"""
        response = self.client.post(reverse('documents:delete', args=[self.document.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(Document.objects.filter(pk=self.document.pk).exists())


class EventsViewsTest(TestCase):
    """Pruebas para las vistas de eventos"""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.event = Event.objects.create(
            title="Evento de prueba",
            description="Descripción del evento",
            date="2024-12-25",
            time="18:00:00",
            location="Iglesia Principal"
        )

    def test_event_list_view(self):
        """Prueba la vista de lista de eventos"""
        response = self.client.get(reverse('events:events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/events.html')
        self.assertContains(response, "Evento de prueba")

    def test_event_create_view_get(self):
        """Prueba la vista de creación de evento (GET)"""
        response = self.client.get(reverse('events:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create.html')

    def test_event_create_view_post(self):
        """Prueba la vista de creación de evento (POST)"""
        data = {
            'title': 'Nuevo evento',
            'description': 'Descripción del nuevo evento',
            'date': '2024-12-26',
            'time': '19:00:00',
            'location': 'Salón Principal'
        }
        response = self.client.post(reverse('events:create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Event.objects.filter(title='Nuevo evento').exists())

    def test_event_edit_view_get(self):
        """Prueba la vista de edición de evento (GET)"""
        response = self.client.get(reverse('events:edit', args=[self.event.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create.html')
        self.assertContains(response, "Evento de prueba")

    def test_event_edit_view_post(self):
        """Prueba la vista de edición de evento (POST)"""
        data = {
            'title': 'Evento actualizado',
            'description': 'Descripción actualizada',
            'date': '2024-12-25',
            'time': '20:00:00',
            'location': 'Iglesia Principal'
        }
        response = self.client.post(reverse('events:edit', args=[self.event.pk]), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Evento actualizado')

    def test_event_delete_view_get(self):
        """Prueba la vista de eliminación de evento (GET)"""
        response = self.client.get(reverse('events:delete', args=[self.event.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/confirm_delete.html')

    def test_event_delete_view_post(self):
        """Prueba la vista de eliminación de evento (POST)"""
        response = self.client.post(reverse('events:delete', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())


class DonationsViewsTest(TestCase):
    """Pruebas para las vistas de donaciones"""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.donation_type = DonationType.objects.create(name="Monetaria")
        self.donation = Donation.objects.create(
            title="Donación de prueba",
            donation_type=self.donation_type,
            amount=Decimal('100.00'),
            description="Descripción de la donación",
            method="deposito",
            entity="Banco de México",
            created_by=self.user
        )

    def test_donation_list_view(self):
        """Prueba la vista de lista de donaciones"""
        response = self.client.get(reverse('donations:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/donations.html')
        self.assertContains(response, "Donación de prueba")

    def test_donation_create_view_get(self):
        """Prueba la vista de creación de donación (GET)"""
        response = self.client.get(reverse('donations:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/create.html')

    def test_donation_create_view_post(self):
        """Prueba la vista de creación de donación (POST)"""
        data = {
            'title': 'Nueva donación',
            'donation_type': self.donation_type.id,
            'amount': '200.00',
            'description': 'Descripción de la nueva donación',
            'method': 'transferencia',
            'entity': 'Banco Santander'
        }
        response = self.client.post(reverse('donations:create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Donation.objects.filter(title='Nueva donación').exists())

    def test_donation_edit_view_get(self):
        """Prueba la vista de edición de donación (GET)"""
        response = self.client.get(reverse('donations:edit', args=[self.donation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/create.html')
        self.assertContains(response, "Donación de prueba")

    def test_donation_edit_view_post(self):
        """Prueba la vista de edición de donación (POST)"""
        data = {
            'title': 'Donación actualizada',
            'donation_type': self.donation_type.id,
            'amount': '150.00',
            'description': 'Descripción actualizada',
            'method': 'deposito',
            'entity': 'Banco de México'
        }
        response = self.client.post(reverse('donations:edit', args=[self.donation.pk]), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.donation.refresh_from_db()
        self.assertEqual(self.donation.title, 'Donación actualizada')

    def test_donation_delete_view_get(self):
        """Prueba la vista de eliminación de donación (GET)"""
        response = self.client.get(reverse('donations:delete', args=[self.donation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/confirm_delete.html')

    def test_donation_delete_view_post(self):
        """Prueba la vista de eliminación de donación (POST)"""
        response = self.client.post(reverse('donations:delete', args=[self.donation.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(Donation.objects.filter(pk=self.donation.pk).exists())


class DashboardViewsTest(TestCase):
    """Pruebas para las vistas del dashboard"""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_dashboard_home_view(self):
        """Prueba la vista del dashboard principal"""
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')


class UserSettingsViewsTest(TestCase):
    """Pruebas para las vistas de configuración de usuario"""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_profile_view(self):
        """Prueba la vista de perfil de usuario"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_settings:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_settings/profile.html') 