import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_products_list_public(client, product):
    """
    Caso 1: acceso sin token -> debe dar 200 (lectura pública).
    """
    url = reverse("product-list")
    response = client.get(url)

    # Lectura debe estar permitida sin token
    assert response.status_code == 200
    assert "results" in response.data or isinstance(response.data, list)


@pytest.mark.django_db
def test_products_list_with_auth(auth_client, product):
    """
    Caso 2: acceso con token válido -> 200 ok y lista de productos.
    """
    url = reverse("product-list")
    response = auth_client.get(url)

    assert response.status_code == 200
    # Puede ser lista directa o paginada
    assert isinstance(response.data, list) or "results" in response.data


@pytest.mark.django_db
def test_products_write_not_available_even_with_auth(auth_client):
    """
    ReadOnlyModelViewSet: los endpoints de escritura no deben estar disponibles.
    - Si el cliente no está autenticado correctamente → 401
    - Si está autenticado correctamente pero el método no existe → 405
    """
    url = reverse("product-list")
    resp = auth_client.post(
        url,
        {
            "sku": "SKU-TEST",
            "name": "Producto test",
            "price": "123.45",
            "stock": 5,
        },
        format="json",
    )

    # Aceptamos ambos casos según cómo DRF maneje la request
    assert resp.status_code in (401, 405)
