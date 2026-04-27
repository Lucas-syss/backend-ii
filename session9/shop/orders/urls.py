from django.urls import path
from . import views

urlpatterns = [
    path("cart/<int:user_id>/", views.cart_detail, name="cart-detail"),
    path("cart/<int:user_id>/add/", views.add_to_cart, name="add-to-cart"),
    path("<int:order_id>/buy/", views.buy, name="buy"),
]