from django.http import JsonResponse
from .models import Product


def product_list(request):
    products = list(Product.objects.values("id", "name", "price"))
    return JsonResponse(products, safe=False)