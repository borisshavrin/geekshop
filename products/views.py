from django.shortcuts import render

import json

# controllers = views = функции


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
    with open('products/fixtures/products_list.json', encoding='UTF-8') as file:
        products_json = json.load(file)
        products_list = products_json['products']
        context['products'] = products_list
    return render(request, 'products/products.html', context)
