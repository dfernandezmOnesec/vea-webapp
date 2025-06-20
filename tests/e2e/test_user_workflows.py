"""
Pruebas end-to-end para flujos de usuario
"""
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


class UserWorkflowTest(TestCase):
    """Pruebas de flujos de trabajo completos de usuario"""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.donation_type = DonationType.objects.create(name="Monetaria")

    def test_complete_contact_workflow(self):
        """Prueba el flujo completo de gestión de contactos"""
        # 1. Acceder a la lista de contactos
        response = self.client.get(reverse('directory:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'directory/directory.html')

        # 2. Crear un nuevo contacto
        contact_data = {
            'name': 'María González',
            'role': 'Líder de Ministerio',
            'ministry': 'Ministerio de Mujeres',
            'contact': 'maria@iglesia.com'
        }
        response = self.client.post(reverse('directory:create'), contact_data)
        self.assertEqual(response.status_code, 302)  # Redirect después de crear

        # 3. Verificar que el contacto se creó
        contact = Contact.objects.get(first_name='María', last_name='González')
        self.assertEqual(contact.role, 'Líder de Ministerio')
        self.assertEqual(contact.ministry, 'Ministerio de Mujeres')

        # 4. Editar el contacto
        edit_data = {
            'name': 'María González',
            'role': 'Coordinadora de Ministerio',
            'ministry': 'Ministerio de Mujeres',
            'contact': 'maria@iglesia.com'
        }
        response = self.client.post(reverse('directory:edit', args=[contact.pk]), edit_data)
        self.assertEqual(response.status_code, 302)

        # 5. Verificar que se actualizó
        contact.refresh_from_db()
        self.assertEqual(contact.role, 'Coordinadora de Ministerio')

        # 6. Eliminar el contacto
        response = self.client.post(reverse('directory:delete', args=[contact.pk]))
        self.assertEqual(response.status_code, 302)

        # 7. Verificar que se eliminó
        self.assertFalse(Contact.objects.filter(pk=contact.pk).exists())

    def test_complete_document_workflow(self):
        """Prueba el flujo completo de gestión de documentos"""
        # 1. Acceder a la lista de documentos
        response = self.client.get(reverse('documents:document_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/documents.html')

        # 2. Crear un nuevo documento
        test_file = SimpleUploadedFile(
            "test_document.pdf",
            b"contenido del archivo de prueba",
            content_type="application/pdf"
        )
        document_data = {
            'title': 'Documento de prueba E2E',
            'description': 'Descripción del documento de prueba',
            'category': 'eventos_generales'
        }
        files = {
            'file': test_file
        }
        response = self.client.post(reverse('documents:create'), document_data, files=files)
        self.assertEqual(response.status_code, 302)

        # 3. Verificar que el documento se creó
        document = Document.objects.get(title='Documento de prueba E2E')
        self.assertEqual(document.description, 'Descripción del documento de prueba')
        self.assertEqual(document.category, 'eventos_generales')

        # 4. Editar el documento
        edit_data = {
            'title': 'Documento de prueba E2E Actualizado',
            'description': 'Descripción actualizada',
            'category': 'ministerios'
        }
        response = self.client.post(reverse('documents:edit', args=[document.pk]), edit_data)
        self.assertEqual(response.status_code, 302)

        # 5. Verificar que se actualizó
        document.refresh_from_db()
        self.assertEqual(document.title, 'Documento de prueba E2E Actualizado')
        self.assertEqual(document.category, 'ministerios')

        # 6. Eliminar el documento
        response = self.client.post(reverse('documents:delete', args=[document.pk]))
        self.assertEqual(response.status_code, 302)

        # 7. Verificar que se eliminó
        self.assertFalse(Document.objects.filter(pk=document.pk).exists())

    def test_complete_event_workflow(self):
        """Prueba el flujo completo de gestión de eventos"""
        # 1. Acceder a la lista de eventos
        response = self.client.get(reverse('events:events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/events.html')

        # 2. Crear un nuevo evento
        event_data = {
            'title': 'Evento de prueba E2E',
            'description': 'Descripción del evento de prueba',
            'date': '2024-12-25',
            'time': '18:00:00',
            'location': 'Iglesia Principal'
        }
        response = self.client.post(reverse('events:create'), event_data)
        self.assertEqual(response.status_code, 302)

        # 3. Verificar que el evento se creó
        event = Event.objects.get(title='Evento de prueba E2E')
        self.assertEqual(event.description, 'Descripción del evento de prueba')
        self.assertEqual(str(event.date), '2024-12-25')
        self.assertEqual(str(event.time), '18:00:00')

        # 4. Editar el evento
        edit_data = {
            'title': 'Evento de prueba E2E Actualizado',
            'description': 'Descripción actualizada del evento',
            'date': '2024-12-26',
            'time': '19:00:00',
            'location': 'Salón Principal'
        }
        response = self.client.post(reverse('events:edit', args=[event.pk]), edit_data)
        self.assertEqual(response.status_code, 302)

        # 5. Verificar que se actualizó
        event.refresh_from_db()
        self.assertEqual(event.title, 'Evento de prueba E2E Actualizado')
        self.assertEqual(str(event.date), '2024-12-26')
        self.assertEqual(str(event.time), '19:00:00')

        # 6. Eliminar el evento
        response = self.client.post(reverse('events:delete', args=[event.pk]))
        self.assertEqual(response.status_code, 302)

        # 7. Verificar que se eliminó
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())

    def test_complete_donation_workflow(self):
        """Prueba el flujo completo de gestión de donaciones"""
        # 1. Acceder a la lista de donaciones
        response = self.client.get(reverse('donations:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/donations.html')

        # 2. Crear una nueva donación
        donation_data = {
            'title': 'Donación de prueba E2E',
            'donation_type': self.donation_type.id,
            'amount': '500.00',
            'description': 'Descripción de la donación de prueba',
            'method': 'transferencia',
            'entity': 'Banco Santander',
            'bank': 'Santander',
            'clabe': '014180000000000000',
            'location': 'Sucursal Centro'
        }
        response = self.client.post(reverse('donations:create'), donation_data)
        self.assertEqual(response.status_code, 302)

        # 3. Verificar que la donación se creó
        donation = Donation.objects.get(title='Donación de prueba E2E')
        self.assertEqual(donation.amount, Decimal('500.00'))
        self.assertEqual(donation.method, 'transferencia')
        self.assertEqual(donation.entity, 'Banco Santander')

        # 4. Editar la donación
        edit_data = {
            'title': 'Donación de prueba E2E Actualizada',
            'donation_type': self.donation_type.id,
            'amount': '750.00',
            'description': 'Descripción actualizada de la donación',
            'method': 'deposito',
            'entity': 'Banco de México'
        }
        response = self.client.post(reverse('donations:edit', args=[donation.pk]), edit_data)
        self.assertEqual(response.status_code, 302)

        # 5. Verificar que se actualizó
        donation.refresh_from_db()
        self.assertEqual(donation.title, 'Donación de prueba E2E Actualizada')
        self.assertEqual(donation.amount, Decimal('750.00'))
        self.assertEqual(donation.method, 'deposito')

        # 6. Eliminar la donación
        response = self.client.post(reverse('donations:delete', args=[donation.pk]))
        self.assertEqual(response.status_code, 302)

        # 7. Verificar que se eliminó
        self.assertFalse(Donation.objects.filter(pk=donation.pk).exists())

    def test_cross_module_integration(self):
        """Prueba la integración entre diferentes módulos"""
        # 1. Crear datos en diferentes módulos
        contact = Contact.objects.create(
            name="Pastor Juan",
            role="Pastor Principal",
            ministry="Ministerio General",
            contact="pastor@iglesia.com"
        )

        event = Event.objects.create(
            title="Conferencia General",
            description="Conferencia anual de la iglesia",
            date="2024-12-25",
            time="18:00:00",
            location="Iglesia Principal"
        )

        document = Document.objects.create(
            title="Programa de Conferencia",
            description="Programa detallado de la conferencia",
            category="eventos_generales",
            user=self.user
        )

        donation = Donation.objects.create(
            title="Donación para Conferencia",
            donation_type=self.donation_type,
            amount=Decimal('1000.00'),
            description="Donación para cubrir gastos de la conferencia",
            method="transferencia",
            entity="Banco de México",
            created_by=self.user
        )

        # 2. Verificar que todos los datos están disponibles
        self.assertTrue(Contact.objects.filter(first_name="Pastor", last_name="Juan").exists())
        self.assertTrue(Event.objects.filter(title="Conferencia General").exists())
        self.assertTrue(Document.objects.filter(title="Programa de Conferencia").exists())
        self.assertTrue(Donation.objects.filter(title="Donación para Conferencia").exists())

        # 3. Verificar que las vistas principales muestran los datos
        response = self.client.get(reverse('directory:list'))
        self.assertContains(response, "Pastor Juan")

        response = self.client.get(reverse('events:events'))
        self.assertContains(response, "Conferencia General")

        response = self.client.get(reverse('documents:document_list'))
        self.assertContains(response, "Programa de Conferencia")

        response = self.client.get(reverse('donations:list'))
        self.assertContains(response, "Donación para Conferencia")

    def test_error_handling_workflow(self):
        """Prueba el manejo de errores en flujos de trabajo"""
        # 1. Intentar acceder a un contacto que no existe
        response = self.client.get(reverse('directory:edit', args=[99999]))
        self.assertEqual(response.status_code, 404)

        # 2. Intentar enviar datos inválidos
        invalid_data = {
            'name': '',  # Campo requerido vacío
            'ministry': 'Ministerio de Jóvenes'
        }
        response = self.client.post(reverse('directory:create'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Vuelve al formulario con errores

        # 3. Intentar eliminar un objeto que no existe
        response = self.client.post(reverse('directory:delete', args=[99999]))
        self.assertEqual(response.status_code, 404)

        # 4. Verificar que no se crearon objetos inválidos
        self.assertEqual(Contact.objects.count(), 0) 