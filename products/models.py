from django.db import models


# models = Таблицы.


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    images = models.ImageField(upload_to='products_images', blank=True)
    description = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2),
    quantity = models.PositiveIntegerField(default=0),
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
