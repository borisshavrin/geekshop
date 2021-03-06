from django.db import models

from users.models import User
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    def sum(self):
        return self.quantity * self.product.price

    def total_quantity(self):
        basket = Basket.objects.filter(user=self.user)
        return sum(item.quantity for item in basket)

    def total_sum(self):
        basket = Basket.objects.filter(user=self.user)
        return sum(item.sum() for item in basket)
