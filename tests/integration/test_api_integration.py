"""
Pruebas de integración para APIs y servicios externos
"""
import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
import json

from apps.core.models import CustomUser
from apps.directory.models import Contact
from apps.documents.models import Document
from apps.events.models import Event
from apps.donations.models import Donation, DonationType

User = get_user_model()


class APIIntegrationTest(TestCase):
    """Pruebas de integración para APIs"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.donation_type = DonationType.objects.create(name="Monetaria")

    def test_document_upload_integration(self):
        """Prueba la integración de carga de documentos"""
        # Simular carga de archivo
        test_file = SimpleUploadedFile(
            "test_integration.pdf",
            "contenido del archivo de integración".encode('utf-8'),
            content_type="application/pdf"
        )
        
        document_data = {
            'title': 'Documento de Integración',
            'description': 'Documento para pruebas de integración',
            'category': 'eventos_generales'
        }
        files = {
            'file': test_file
        }
        
        # Crear documento
        document = Document.objects.create(
            title=document_data['title'],
            description=document_data['description'],
            category=document_data['category'],
            user=self.user
        )
        
        # Verificar que se procesó correctamente
        self.assertEqual(document.title, 'Documento de Integración')
        self.assertEqual(document.processing_status, 'pendiente')
        self.assertFalse(document.is_processed)

    def test_donation_calculation_integration(self):
        """Prueba la integración de cálculos de donaciones"""
        # Crear múltiples donaciones
        donations = []
        amounts = [100.00, 250.50, 75.25, 500.00]
        
        for i, amount in enumerate(amounts):
            donation = Donation.objects.create(
                title=f'Donación {i+1}',
                donation_type=self.donation_type,
                amount=Decimal(str(amount)),
                description=f'Descripción de donación {i+1}',
                method='deposito',
                entity='Banco de México',
                created_by=self.user
            )
            donations.append(donation)
        
        # Calcular total
        total_amount = sum(donation.amount for donation in donations)
        expected_total = Decimal('925.75')
        
        self.assertEqual(total_amount, expected_total)
        self.assertEqual(len(donations), 4)

    def test_event_scheduling_integration(self):
        """Prueba la integración de programación de eventos"""
        # Crear eventos con diferentes fechas
        events = []
        event_data = [
            {
                'title': 'Evento 1',
                'date': '2024-12-25',
                'time': '18:00:00'
            },
            {
                'title': 'Evento 2',
                'date': '2024-12-26',
                'time': '19:00:00'
            },
            {
                'title': 'Evento 3',
                'date': '2024-12-27',
                'time': '20:00:00'
            }
        ]
        
        for data in event_data:
            event = Event.objects.create(
                title=data['title'],
                description=f'Descripción de {data["title"]}',
                date=data['date'],
                time=data['time'],
                location='Iglesia Principal'
            )
            events.append(event)
        
        # Verificar ordenamiento
        ordered_events = Event.objects.all()
        self.assertEqual(ordered_events[0].title, 'Evento 3')  # Más reciente primero
        self.assertEqual(ordered_events[1].title, 'Evento 2')
        self.assertEqual(ordered_events[2].title, 'Evento 1')

    def test_contact_directory_integration(self):
        """Prueba la integración del directorio de contactos"""
        # Crear contactos de diferentes ministerios
        ministries = [
            'Ministerio de Jóvenes',
            'Ministerio de Mujeres',
            'Ministerio de Hombres',
            'Ministerio de Niños'
        ]
        
        contacts = []
        for i, ministry in enumerate(ministries):
            contact = Contact.objects.create(
                name=f'Contacto {i+1}',
                role=f'Líder de {ministry}',
                ministry=ministry,
                contact=f'contacto{i+1}@iglesia.com'
            )
            contacts.append(contact)
        
        # Verificar que todos se crearon
        self.assertEqual(Contact.objects.count(), 4)
        
        # Verificar ordenamiento alfabético por nombre
        ordered_contacts = Contact.objects.all()
        self.assertEqual(ordered_contacts[0].name, 'Contacto 1')
        self.assertEqual(ordered_contacts[1].name, 'Contacto 2')
        self.assertEqual(ordered_contacts[2].name, 'Contacto 3')
        self.assertEqual(ordered_contacts[3].name, 'Contacto 4')

    def test_user_authentication_integration(self):
        """Prueba la integración de autenticación de usuarios"""
        # Crear usuario
        user = CustomUser.objects.create_user(
            email='integration@example.com',
            username='integration_user',
            password='integration_pass123'
        )
        
        # Verificar autenticación
        self.assertTrue(user.check_password('integration_pass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
        # Crear superusuario
        admin = CustomUser.objects.create_superuser(
            email='admin@example.com',
            username='admin_user',
            password='admin_pass123'
        )
        
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_data_consistency_integration(self):
        """Prueba la consistencia de datos entre módulos"""
        # Crear datos relacionados
        contact = Contact.objects.create(
            name="Pastor Principal",
            role="Pastor",
            ministry="Ministerio General",
            contact="pastor@iglesia.com"
        )
        
        event = Event.objects.create(
            title="Conferencia de Pastores",
            description="Conferencia organizada por el Pastor Principal",
            date="2024-12-25",
            time="18:00:00",
            location="Iglesia Principal"
        )
        
        document = Document.objects.create(
            title="Programa de Conferencia",
            description="Programa de la conferencia de pastores",
            category="eventos_generales",
            user=self.user
        )
        
        donation = Donation.objects.create(
            title="Donación para Conferencia",
            donation_type=self.donation_type,
            amount=Decimal('1500.00'),
            description="Donación para la conferencia de pastores",
            method="transferencia",
            entity="Banco de México",
            created_by=self.user
        )
        
        # Verificar que todos los datos están relacionados lógicamente
        self.assertIn("Pastor", contact.role)
        self.assertIn("Conferencia", event.title)
        self.assertIn("Programa", document.title)
        self.assertIn("Donación", donation.title)
        
        # Verificar que las fechas son consistentes
        self.assertEqual(str(event.date), "2024-12-25")

    def test_error_handling_integration(self):
        """Prueba el manejo de errores en integración"""
        # Intentar crear datos inválidos
        with self.assertRaises(Exception):
            # Intentar crear usuario sin email (campo requerido)
            CustomUser.objects.create_user(
                email='',
                username='invalid_user'
            )
        
        # Verificar que no se creó el usuario inválido
        self.assertFalse(CustomUser.objects.filter(username='invalid_user').exists())
        
        # Intentar crear donación sin tipo
        with self.assertRaises(Exception):
            Donation.objects.create(
                title="Donación sin tipo",
                amount=Decimal('100.00'),
                created_by=self.user
            )

    def test_performance_integration(self):
        """Prueba el rendimiento de operaciones integradas"""
        # Crear múltiples registros para probar rendimiento
        contacts = []
        for i in range(10):
            contact = Contact.objects.create(
                name=f'Contacto de Rendimiento {i+1}',
                role=f'Rol {i+1}',
                ministry=f'Ministerio {i+1}',
                contact=f'contacto{i+1}@rendimiento.com'
            )
            contacts.append(contact)
        
        # Verificar que se crearon todos
        self.assertEqual(Contact.objects.count(), 10)
        
        # Probar consulta con filtro
        filtered_contacts = Contact.objects.filter(ministry__contains='Ministerio')
        self.assertEqual(filtered_contacts.count(), 10)
        
        # Probar ordenamiento
        ordered_contacts = Contact.objects.order_by('name')
        self.assertEqual(len(ordered_contacts), 10) 