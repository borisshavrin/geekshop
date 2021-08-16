import os.path
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache

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


def products(request, category_id=None, page=1):
    context = {'title': 'GeekShop', 'categories': get_links_menu()}
    products = get_products_in_category_ordered_by_price(category_id) if category_id else get_products()

    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context.update({'products': products_paginator})

    if ProductCategory.objects.count() == 0 or Product.objects.count() == 0:
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


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.all()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.all()


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True).order_by('price')
