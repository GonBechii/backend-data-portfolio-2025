import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse


@pytest.fixture
def api_client():
    """ Cliente DRF sin autenticación. """
    return APIClient()


@pytest.fixture
def user(db):
    """ Usuario de prueba genérico """
    return User.objects.create_user(username="tester", password="pass12345")


@pytest.fixture
def auth_client(api_client, user):
    """
    Cliente autenticado con JWT
    Usa el endpoint de Simple JWT (token_obtain_pair).   
    """
    url = reverse("token_obtain_pair")
    response = api_client.post(
        url, {"username": "tester", "password": "pass12345"}, format="json"
    )
    assert response.status_code == 200, "No se pudo autenticar en fixture: {response.data}"
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture
def product(db):
    """ Producto de prueba creado con el model_bakery """
    return baker.make("core.Product", stock=10)
