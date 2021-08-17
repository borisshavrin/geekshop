from django.test import TestCase
from products.models import Product, ProductCategory


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="Головные Уборы")
        self.product_1 = Product.objects.create(name="Кепка",
                                                category=category,
                                                price=1999.5,
                                                quantity=150)

        self.product_2 = Product.objects.create(name="Шапка",
                                                category=category,
                                                price=2998.1,
                                                quantity=125,
                                                is_active=False)

        self.product_3 = Product.objects.create(name="Панамка",
                                                category=category,
                                                price=998.1,
                                                quantity=115)

    def test_product_get(self):
        product_1 = Product.objects.get(name="Кепка")
        product_2 = Product.objects.get(name="Шапка")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="Кепка")
        product_2 = Product.objects.get(name="Шапка")
        self.assertEqual(str(product_1), 'Кепка | Головные Уборы')
        self.assertEqual(str(product_2), 'Шапка | Головные Уборы')

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="Кепка")
        product_3 = Product.objects.get(name="Панамка")
        products = product_1.get_items()

        self.assertEqual(list(products), [product_1, product_3])
