import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from products.models import Product
from .models import Order


def _get_or_create_cart(user):
    order, _ = Order.objects.get_or_create(user=user, paid=False)
    return order


def cart_detail(request, user_id):
    user = User.objects.get(pk=user_id)
    order = _get_or_create_cart(user)
    products = list(order.cart.values("id", "name", "price"))
    return JsonResponse({"order_id": order.pk, "cart": products, "total": str(order.total)})


@require_POST
def add_to_cart(request, user_id):
    data = json.loads(request.body)
    product_id = data["product_id"]
    user = User.objects.get(pk=user_id)
    product = Product.objects.get(pk=product_id)
    order = _get_or_create_cart(user)
    order.cart.add(product)
    order.recalculate_total()
    return JsonResponse({"message": "Product added", "total": str(order.total)})


@require_POST
def buy(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.paid = True
    order.save()
    return JsonResponse({"message": "Purchase successful", "order_id": order.pk, "total": str(order.total)})