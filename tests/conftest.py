"""
Configuración de pytest y fixtures comunes para todas las pruebas
"""
import pytest
from django.test import Client


@pytest.fixture
def client():
    """Cliente de Django para pruebas"""
    return Client()


@pytest.fixture
@pytest.mark.django_db
def test_user():
    """Usuario de prueba"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
@pytest.mark.django_db
def admin_user():
    """Usuario administrador de prueba"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
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
@pytest.mark.django_db
def sample_contact():
    """Contacto de prueba"""
    from apps.directory.models import Contact
    return Contact.objects.create(
        first_name="Juan",
        last_name="Pérez",
        role="Pastor",
        ministry="Ministerio de Jóvenes",
        contact="juan@iglesia.com"
    )


@pytest.fixture
@pytest.mark.django_db
def sample_document(test_user):
    """Documento de prueba"""
    from apps.documents.models import Document
    return Document.objects.create(
        title="Documento de prueba",
        description="Descripción de prueba",
        category="eventos_generales",
        user=test_user
    )


@pytest.fixture
@pytest.mark.django_db
def sample_event():
    """Evento de prueba"""
    from apps.events.models import Event
    return Event.objects.create(
        title="Evento de prueba",
        description="Descripción del evento",
        date="2024-12-25",
        time="18:00:00",
        location="Iglesia Principal"
    )


@pytest.fixture
@pytest.mark.django_db
def sample_donation_type():
    """Tipo de donación de prueba"""
    from apps.donations.models import DonationType
    return DonationType.objects.create(name="Monetaria")


@pytest.fixture
@pytest.mark.django_db
def sample_donation(test_user, sample_donation_type):
    """Donación de prueba"""
    from apps.donations.models import Donation
    return Donation.objects.create(
        title="Donación de prueba",
        donation_type=sample_donation_type,
        amount=100.00,
        description="Descripción de la donación",
        method="deposito",
        entity="Banco de México",
        created_by=test_user
    ) 