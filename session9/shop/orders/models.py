from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Product)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def recalculate_total(self):
        self.total = sum(p.price for p in self.cart.all())
        self.save()

    def __str__(self):
        return f"Order #{self.pk} - {self.user} - paid={self.paid}"