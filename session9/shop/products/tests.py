import pytest
from .models import Product


@pytest.mark.django_db
def test_product_list_empty(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_product_list_returns_products(client):
    Product.objects.create(name="Notebook", price="2.99")
    Product.objects.create(name="Pen", price="0.99")

    response = client.get("/products/")
    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Notebook"
    assert data[1]["name"] == "Pen"