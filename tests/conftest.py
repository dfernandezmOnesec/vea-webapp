"""
Configuración de pytest y fixtures comunes para todas las pruebas
"""
import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from apps.core.models import CustomUser
from apps.directory.models import Contact
from apps.documents.models import Document
from apps.events.models import Event
from apps.donations.models import Donation, DonationType

User = get_user_model()


@pytest.fixture
def client():
    """Cliente de Django para pruebas"""
    return Client()


@pytest.fixture
def test_user():
    """Usuario de prueba"""
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
def admin_user():
    """Usuario administrador de prueba"""
    return User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='adminpass123'
    )


@pytest.fixture
def authenticated_client(client, test_user):
    """Cliente autenticado con usuario de prueba"""
    client.force_login(test_user)
    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Cliente autenticado con usuario administrador"""
    client.force_login(admin_user)
    return client


@pytest.fixture
def sample_contact():
    """Contacto de prueba"""
    return Contact.objects.create(
        first_name="Juan",
        last_name="Pérez",
        role="Pastor",
        ministry="Ministerio de Jóvenes",
        contact="juan@iglesia.com"
    )


@pytest.fixture
def sample_document(test_user):
    """Documento de prueba"""
    return Document.objects.create(
        title="Documento de prueba",
        description="Descripción de prueba",
        category="eventos_generales",
        user=test_user
    )


@pytest.fixture
def sample_event():
    """Evento de prueba"""
    return Event.objects.create(
        title="Evento de prueba",
        description="Descripción del evento",
        date="2024-12-25",
        time="18:00:00",
        location="Iglesia Principal"
    )


@pytest.fixture
def sample_donation_type():
    """Tipo de donación de prueba"""
    return DonationType.objects.create(name="Monetaria")


@pytest.fixture
def sample_donation(test_user, sample_donation_type):
    """Donación de prueba"""
    return Donation.objects.create(
        title="Donación de prueba",
        donation_type=sample_donation_type,
        amount=100.00,
        description="Descripción de la donación",
        method="deposito",
        entity="Banco de México",
        created_by=test_user
    ) 