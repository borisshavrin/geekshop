import os.path
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection

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


def products_ajax(request, category_id=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()

        if category_id:
            if category_id == '0':
                category = {
                    'category_id': 0
                }
                products = get_products_ordered_by_price()
            else:
                category = get_category(category_id)
                products = get_products_in_category_ordered_by_price(category_id)

            paginator = Paginator(products, 2)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)

            content = {
                'links_menu': links_menu,
                'category': category,
                'products': products_paginator,
            }

            result = render_to_string(
                'products/products.html',
                context=content,
                request=request)

            return JsonResponse({'result': result})


def db_profile_by_type(prefix, type, queries):
    """Ф-ия отфильтровывает запросы определенного типа (например, «UPDATE», «DELETE», «SELECT», «INSERT INTO»)"""
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    """Вместо работы с методами классов «ProductCategoryUpdateView()» и «ProductCategoryDeleteView()»
        воспользовались механизмом сигналов - так будет меньше кода.  Атрибут «product_set Django»
        создан автоматически для связи с моделью Product по внешнему ключу. В этом атрибуте получаем QuerySet,
        который позволяет получить все продукты в данной категории и применяем к нему метод «.update()»."""
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
