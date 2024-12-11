from django.db import models

from goods.models import Products
from users.models import User


class CartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartQueryset().as_manager()


    def products_price(self):
        return round(self.product.display_price_with_discount() * self.quantity, 2)
        

    def __str__(self):
        if self.user:
            return f'Cart {self.user.username} | Product {self.product.name} | Quantity {self.quantity}'
        return f'Anonymous cart | Product {self.product.name} | Quantity {self.quantity}'