import os.path
from django.shortcuts import render
import json
from products.models import Product, ProductCategory

# controllers = views = функции
MODULE_DIR = os.path.dirname(__file__)


def index(request):
    context = {
        'title': 'GeekShop',
        'heading_name': 'geekShop store',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    context = {'title': 'GeekShop', 'categories': ProductCategory.objects.all()}
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    context.update({'products': products})

    if ProductCategory.objects.count() == 0 and Product.objects.count() == 0:
        load_database_from_fixtures()

    return render(request, 'products/products.html', context)


def load_database_from_fixtures():
    # при создании фикстур pycharm ругается на кодировку и просит перевести ее в windows-1251
    category_file_path = os.path.join(MODULE_DIR, 'fixtures/category.json')
    category_file_json = open(category_file_path, encoding='windows-1251')
    category_list = json.load(category_file_json)

    for category_dict in category_list:
        category = category_dict['fields']
        db_product = ProductCategory(name=category['name'], description=category['description'])
        db_product.save()

    goods_file_path = os.path.join(MODULE_DIR, 'fixtures/goods.json')
    goods_file_json = open(goods_file_path, encoding='windows-1251')
    goods_list = json.load(goods_file_json)

    for goods_dict in goods_list:
        goods = goods_dict['fields']
        category_id = ProductCategory.objects.get(id=goods['category'])
        db_product = Product(name=goods['name'], images=goods['images'], description=goods['description'],
                             price=goods['price'], quantity=goods['quantity'], category=category_id)
        db_product.save()
