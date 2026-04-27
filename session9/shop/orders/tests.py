import json
import pytest
from django.contrib.auth.models import User
from products.models import Product
from .models import Order


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="pass")


@pytest.fixture
def product(db):
    return Product.objects.create(name="Notebook", price="2.99")


@pytest.fixture
def another_product(db):
    return Product.objects.create(name="Pen", price="0.99")



@pytest.mark.django_db
def test_cart_starts_empty(client, user):
    response = client.get(f"/orders/cart/{user.pk}/")
    assert response.status_code == 200
    data = response.json()
    assert data["cart"] == []
    assert data["total"] == "0"


@pytest.mark.django_db
def test_add_product_to_cart(client, user, product):
    response = client.post(
        f"/orders/cart/{user.pk}/add/",
        data=json.dumps({"product_id": product.pk}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json()["total"] == "2.99"


@pytest.mark.django_db
def test_cart_lists_added_products(client, user, product, another_product):
    client.post(
        f"/orders/cart/{user.pk}/add/",
        data=json.dumps({"product_id": product.pk}),
        content_type="application/json",
    )
    client.post(
        f"/orders/cart/{user.pk}/add/",
        data=json.dumps({"product_id": another_product.pk}),
        content_type="application/json",
    )
    response = client.get(f"/orders/cart/{user.pk}/")
    data = response.json()
    assert len(data["cart"]) == 2
    assert data["total"] == "3.98"


@pytest.mark.django_db
def test_buy_marks_order_as_paid(client, user, product):
    client.post(
        f"/orders/cart/{user.pk}/add/",
        data=json.dumps({"product_id": product.pk}),
        content_type="application/json",
    )
    order = Order.objects.get(user=user, paid=False)
    response = client.post(f"/orders/{order.pk}/buy/")
    assert response.status_code == 200
    assert response.json()["message"] == "Purchase successful"
    order.refresh_from_db()
    assert order.paid is True