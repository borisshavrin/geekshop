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
        products_dict = json.load(file)
        for item, desc in products_dict.items():
            context[item] = desc
    return render(request, 'products/products.html', context)


def base(request):
    return render(request, 'products/base.html')
