# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from products.models import Product, ProductCategory
from django.core.management import call_command



class TestProductsSmoke(TestCase):

    def setUp(self) -> None:
        """Очищаем базу и импортируем данные"""
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()                      # объект класса «Client» для отправки запросов

    def test_products_urls(self):
        """Подготавливаем и проверяем данные"""
        """Для проверки соответствия реального и ожидаемого значения в тестах 
            используем метод «.assertEqual() класса TestCase»."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/0/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        # for product in Product.objects.all():
        #     response = self.client.get(f'/products/product/{product.pk}/')
        #     self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """Команда сброса индексов"""
        call_command('sqlsequencereset', 'basket', 'orders', 'products', 'users')

