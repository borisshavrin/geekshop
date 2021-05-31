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
        products_list = json.load(file)
        for idx, description in enumerate(products_list, start=1):
            item = f'item_{idx}'
            context[item] = description
    return render(request, 'products/products.html', context)
