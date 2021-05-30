from django.shortcuts import render

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
        'products_list': {
            'item_1': {
                'name': 'Худи черного цвета с монограммами adidas Originals',
                'price': 6090,
                'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.'
            },
            'item_2': {
                'name': 'Синяя куртка The North Face',
                'price': 23725,
                'description': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.'
            },
            'item_3': {
                'name': 'Коричневый спортивный oversized-топ ASOS DESIGN',
                'price': 3390,
                'description': 'Материал с плюшевой текстурой. Удобный и мягкий.'
            },
            'item_4': {
                'name': 'Черный рюкзак Nike Heritage',
                'price': 2340,
                'description': 'Плотная ткань. Легкий материал.'
            },
            'item_5': {
                'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
                'price': 13590,
                'description': 'Гладкий кожаный верх. Натуральный материал.'
            },
            'item_6': {
                'name': 'Темно-синие широкие строгие брюки ASOS DESIGN',
                'price': 2890,
                'description': 'Легкая эластичная ткань сирсакер Фактурная ткань.'
            }
        },
    }
    return render(request, 'products/products.html', context)


def base(request):
    return render(request, 'products/base.html')
