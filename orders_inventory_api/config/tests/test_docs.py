from django.urls import reverse


def test_swagger_ui_loads(client):
    """
        Verifica que Swagger UI (/api/docs) carga correctamente
    """
    url = reverse("swagger-ui")
    resp = client.get(url)
    assert resp.status_code == 200
