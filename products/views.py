import os.path
from django.shortcuts import render
import json

# controllers = views = функции
MODULE_DIR = os.path.dirname(__file__)


def index(request):
    context = {
        'title': 'GeekShop',
        'heading_name': 'geekShop store',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'GeekShop',
    }
    file_path = os.path.join(MODULE_DIR, 'fixtures/products_list.json')
    file_json = open(file_path, encoding='utf-8')
    products_list = json.load(file_json)
    context['products'] = products_list['products']
    return render(request, 'products/products.html', context)
