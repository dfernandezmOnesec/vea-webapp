"""
Pruebas unitarias para los modelos de la aplicación
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta


class CustomUserModelTest(TestCase):
    """Pruebas para el modelo CustomUser"""

    def test_create_user(self):
        """Prueba la creación de un usuario normal"""
        from apps.core.models import CustomUser
        user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Prueba la creación de un superusuario"""
        from apps.core.models import CustomUser
        admin = CustomUser.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_string_representation(self):
        """Prueba la representación en string del usuario"""
        from apps.core.models import CustomUser
        user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser'
        )
        self.assertEqual(str(user), 'test@example.com')

    def test_user_email_unique(self):
        """Prueba que el email sea único"""
        from apps.core.models import CustomUser
        CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser1'
        )
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                email='test@example.com',
                username='testuser2'
            )


class ContactModelTest(TestCase):
    """Pruebas para el modelo Contact"""

    def test_create_contact(self):
        """Prueba la creación de un contacto"""
        from apps.directory.models import Contact
        contact = Contact.objects.create(
            first_name="Juan",
            last_name="Pérez",
            role="Pastor",
            ministry="Ministerio de Jóvenes",
            contact="juan@iglesia.com"
        )
        self.assertEqual(contact.first_name, "Juan")
        self.assertEqual(contact.last_name, "Pérez")
        self.assertEqual(contact.role, "Pastor")
        self.assertEqual(contact.ministry, "Ministerio de Jóvenes")
        self.assertEqual(contact.contact, "juan@iglesia.com")
        self.assertIsNotNone(contact.created_at)

    def test_contact_string_representation(self):
        """Prueba la representación en string del contacto"""
        from apps.directory.models import Contact
        contact = Contact.objects.create(
            first_name="Juan",
            last_name="Pérez",
            ministry="Ministerio de Jóvenes",
            contact="juan@iglesia.com"
        )
        self.assertEqual(str(contact), "Juan Pérez")

    def test_contact_ordering(self):
        """Prueba el ordenamiento de contactos por apellido y nombre"""
        from apps.directory.models import Contact
        contact2 = Contact.objects.create(
            first_name="Ana",
            last_name="García",
            ministry="Ministerio de Mujeres",
            contact="ana@iglesia.com"
        )
        contact1 = Contact.objects.create(
            first_name="Juan",
            last_name="Pérez",
            ministry="Ministerio de Jóvenes",
            contact="juan@iglesia.com"
        )
        contacts = Contact.objects.all()
        self.assertEqual(contacts[0], contact2)  # Ana García (García < Pérez alfabéticamente)
        self.assertEqual(contacts[1], contact1)  # Juan Pérez


class DocumentModelTest(TestCase):
    """Pruebas para el modelo Document"""

    def setUp(self):
        from apps.core.models import CustomUser
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser'
        )

    def test_create_document(self):
        """Prueba la creación de un documento"""
        from apps.documents.models import Document
        document = Document.objects.create(
            title="Documento de prueba",
            description="Descripción de prueba",
            category="eventos_generales",
            user=self.user
        )
        self.assertEqual(document.title, "Documento de prueba")
        self.assertEqual(document.description, "Descripción de prueba")
        self.assertEqual(document.category, "eventos_generales")
        self.assertEqual(document.user, self.user)
        self.assertFalse(document.is_processed)
        self.assertEqual(document.processing_status, "pendiente")

    def test_document_string_representation(self):
        """Prueba la representación en string del documento"""
        from apps.documents.models import Document
        document = Document.objects.create(
            title="Documento de prueba",
            category="eventos_generales",
            user=self.user
        )
        self.assertEqual(str(document), "Documento de prueba")

    def test_document_ordering(self):
        """Prueba el ordenamiento de documentos por fecha"""
        from apps.documents.models import Document
        # Crear documentos con fechas diferentes
        old_date = timezone.now() - timedelta(days=1)
        recent_date = timezone.now()
        
        document1 = Document.objects.create(
            title="Documento antiguo",
            category="eventos_generales",
            user=self.user,
            date=old_date
        )
        document2 = Document.objects.create(
            title="Documento reciente",
            category="ministerios",
            user=self.user,
            date=recent_date
        )
        documents = Document.objects.all()
        self.assertEqual(documents[0], document2)  # Más reciente primero
        self.assertEqual(documents[1], document1)  # Más antiguo después

    def test_document_category_choices(self):
        """Prueba las opciones de categoría válidas"""
        from apps.documents.models import Document
        valid_categories = [
            "eventos_generales",
            "ministerios", 
            "formacion",
            "campanas",
            "avisos_globales"
        ]
        for category in valid_categories:
            document = Document.objects.create(
                title=f"Documento {category}",
                category=category,
                user=self.user
            )
            self.assertEqual(document.category, category)


class EventModelTest(TestCase):
    """Pruebas para el modelo Event"""

    def test_create_event(self):
        """Prueba la creación de un evento"""
        from apps.events.models import Event
        event = Event.objects.create(
            title="Evento de prueba",
            description="Descripción del evento",
            date="2024-12-25",
            time="18:00:00",
            location="Iglesia Principal"
        )
        self.assertEqual(event.title, "Evento de prueba")
        self.assertEqual(event.description, "Descripción del evento")
        self.assertEqual(str(event.date), "2024-12-25")
        self.assertEqual(str(event.time), "18:00:00")
        self.assertEqual(event.location, "Iglesia Principal")
        self.assertIsNotNone(event.created_at)
        self.assertIsNotNone(event.updated_at)

    def test_event_string_representation(self):
        """Prueba la representación en string del evento"""
        from apps.events.models import Event
        event = Event.objects.create(
            title="Evento de prueba",
            date="2024-12-25"
        )
        self.assertEqual(str(event), "Evento de prueba - 2024-12-25")

    def test_event_ordering(self):
        """Prueba el ordenamiento de eventos por fecha y hora"""
        from apps.events.models import Event
        event1 = Event.objects.create(
            title="Evento antiguo",
            date="2024-12-24",
            time="18:00:00"
        )
        event2 = Event.objects.create(
            title="Evento reciente",
            date="2024-12-25",
            time="19:00:00"
        )
        events = Event.objects.all()
        self.assertEqual(events[0], event2)  # Más reciente primero
        self.assertEqual(events[1], event1)  # Más antiguo después


class DonationTypeModelTest(TestCase):
    """Pruebas para el modelo DonationType"""

    def test_create_donation_type(self):
        """Prueba la creación de un tipo de donación"""
        from apps.donations.models import DonationType
        donation_type = DonationType.objects.create(name="Monetaria")
        self.assertEqual(donation_type.name, "Monetaria")

    def test_donation_type_string_representation(self):
        """Prueba la representación en string del tipo de donación"""
        from apps.donations.models import DonationType
        donation_type = DonationType.objects.create(name="En especie")
        self.assertEqual(str(donation_type), "En especie")

    def test_donation_type_unique_name(self):
        """Prueba que el nombre del tipo de donación sea único"""
        from apps.donations.models import DonationType
        DonationType.objects.create(name="Monetaria")
        with self.assertRaises(Exception):
            DonationType.objects.create(name="Monetaria")


class DonationModelTest(TestCase):
    """Pruebas para el modelo Donation"""

    def setUp(self):
        from apps.core.models import CustomUser
        from apps.donations.models import DonationType
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser'
        )
        self.donation_type = DonationType.objects.create(name="Monetaria")

    def test_create_donation(self):
        """Prueba la creación de una donación"""
        from apps.donations.models import Donation
        donation = Donation.objects.create(
            title="Donación de prueba",
            donation_type=self.donation_type,
            amount=Decimal('100.00'),
            description="Descripción de la donación",
            method="deposito",
            entity="Banco de México",
            bank="Banamex",
            clabe="012345678901234567",
            location="Sucursal Centro",
            created_by=self.user
        )
        self.assertEqual(donation.title, "Donación de prueba")
        self.assertEqual(donation.donation_type, self.donation_type)
        self.assertEqual(donation.amount, Decimal('100.00'))
        self.assertEqual(donation.description, "Descripción de la donación")
        self.assertEqual(donation.method, "deposito")
        self.assertEqual(donation.entity, "Banco de México")
        self.assertEqual(donation.bank, "Banamex")
        self.assertEqual(donation.clabe, "012345678901234567")
        self.assertEqual(donation.location, "Sucursal Centro")
        self.assertEqual(donation.created_by, self.user)
        self.assertIsNotNone(donation.created_at)

    def test_donation_negative_amount_validation(self):
        """Prueba que no se pueda crear una donación con monto negativo"""
        from apps.donations.models import Donation
        with self.assertRaises(ValidationError):
            donation = Donation(
                title="Donación negativa",
                donation_type=self.donation_type,
                amount=Decimal('-100.00'),
                created_by=self.user
            )
            donation.full_clean()  # Lanzará ValidationError

    def test_donation_string_representation(self):
        """Prueba la representación en string de la donación"""
        from apps.donations.models import Donation
        donation = Donation.objects.create(
            title="Donación de prueba",
            donation_type=self.donation_type,
            created_by=self.user
        )
        expected_str = f"Donación de prueba - {donation.created_at.strftime('%d/%m/%Y')}"
        self.assertEqual(str(donation), expected_str)

    def test_donation_ordering(self):
        """Prueba el ordenamiento de donaciones por fecha de creación"""
        from apps.donations.models import Donation
        donation1 = Donation.objects.create(
            title="Donación antigua",
            donation_type=self.donation_type,
            created_by=self.user
        )
        donation2 = Donation.objects.create(
            title="Donación reciente",
            donation_type=self.donation_type,
            created_by=self.user
        )
        donations = Donation.objects.all()
        self.assertEqual(donations[0], donation2)  # Más reciente primero
        self.assertEqual(donations[1], donation1)  # Más antiguo después

    def test_donation_method_choices(self):
        """Prueba las opciones de método válidas"""
        from apps.donations.models import Donation
        valid_methods = [
            'deposito',
            'transferencia',
            'relaciones_publicas',
            'ministerio',
            'entrega_directa'
        ]
        
        for method in valid_methods:
            donation = Donation.objects.create(
                title=f"Donación {method}",
                donation_type=self.donation_type,
                method=method,
                created_by=self.user
            )
            self.assertEqual(donation.method, method)

    def test_donation_type_choices(self):
        """Prueba las opciones de tipo válidas"""
        from apps.donations.models import DonationType, Donation
        valid_types = [
            'monetaria',
            'especie',
            'medicamentos',
            'voluntariado',
            'otros'
        ]
        for donation_type_name in valid_types:
            donation_type, _ = DonationType.objects.get_or_create(name=donation_type_name)
            donation = Donation.objects.create(
                title=f"Donación {donation_type_name}",
                donation_type=donation_type,
                created_by=self.user
            )
            self.assertEqual(donation.donation_type, donation_type) 