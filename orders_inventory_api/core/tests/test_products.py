import pytest
from decimal import Decimal
from django.urls import reverse
from model_bakery import baker

from orders_inventory_api.core.models import Product, Customer, Order


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
def test_products_list_pagination(auth_client):
    """
        Caso 3: Lista de productos paginada
    """
    baker.make("core.Product", _quantity=15)
    url = reverse("product-list")
    response = auth_client.get(url, {"page": 1})
    assert response.status_code == 200
    assert "count" in response.data
    assert "results" in response.data
    assert "next" in response.data
    assert "previous" in response.data


@pytest.mark.django_db
def test_products_ordering_by_price(auth_client):
    """Caso 4: ordenar productos por precio"""
    baker.make("core.Product", price=100, stock=10)
    baker.make("core.Product", price=50, stock=5)
    url = reverse("product-list")
    response = auth_client.get(url, {"ordering": "price"})
    assert response.status_code == 200

    # convertir a float para comparar correctamente.
    prices = [float(p["price"]) for p in response.data["results"]]
    assert prices == sorted(prices)


@pytest.mark.django_db
def test_order_create_decrements_stock(auth_client):
    """
    Caso 6: POST /api/orders/ decrementa el stock de cada Product
    """
    customer = baker.make(Customer)
    p = baker.make(Product, price=Decimal("25.00"), stock=7)

    url = reverse("order-list")
    payload = {
        "customer": customer.id,
        "items": [{"product": p.id, "quantity": 3}],
    }

    resp = auth_client.post(url, payload, format="json")
    assert resp.status_code == 201

    p.refresh_from_db()
    assert p.stock == 7 - 3, "El stock debe decrementarse según la cantidad pedida"


@pytest.mark.django_db
def test_order_create_totals_ok(auth_client):
    """
    Caso 5: POST /api/orders/ con productos en stock
    - Debe crear el pedido (201)
    - Subtotal y total deben ser correctos (sum(qty * price))
    """
    customer = baker.make(Customer)  # nombre / email autogenerados
    p1 = baker.make(Product, price=Decimal("100.00"), stock=10)
    p2 = baker.make(Product, price=Decimal("50.00"), stock=5)

    url = reverse("order-list")
    payload = {
        "customer": customer.id,
        "items": [
            {"product": p1.id, "quantity": 2},  # 2 * 100 = 200
            {"product": p2.id, "quantity": 1},  # 1 * 50  = 50
        ],
    }

    resp = auth_client.post(url, payload, format="json")
    assert resp.status_code == 201

    # Validamos contra la base de datos (evitamos acoplarnos al formato exacto del serializer)
    order = Order.objects.latest("id")
    expected_subtotal = Decimal("200.00") + Decimal("50.00")
    # Si en tu modelo/serializer aplicas impuestos/descuentos, puedes ajustar aquí.
    expected_total = expected_subtotal

    # Redondeo con dos decimales para evitar falsos negativos por contexto decimal
    assert order.subtotal.quantize(Decimal("0.01")) == expected_subtotal
    assert order.total.quantize(Decimal("0.01")) == expected_total


@pytest.mark.django_db
def test_order_create_insufficient_stock(auth_client):
    """
    Caso 7: POST /api/orders/ con stock insuficiente
    - Debe rechazar la creación (400/409/422 aceptados)
    - No debe modificar stock ni crear Order
    """
    customer = baker.make(Customer)
    p = baker.make(Product, price=Decimal("10.00"), stock=1)

    url = reverse("order-list")
    payload = {
        "customer": customer.id,
        # pide más de lo disponible
        "items": [{"product": p.id, "quantity": 2}],
    }

    resp = auth_client.post(url, payload, format="json")
    assert resp.status_code in (
        400, 409, 422), f"Status inesperado: {resp.status_code} - body: {resp.data}"

    # Aseguramos que no cambió el stock ni se creó una orden válida
    p.refresh_from_db()
    assert p.stock == 1

    assert Order.objects.count(
    ) == 0, "No debería haberse creado ningún pedido con stock insuficiente"


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
