from django.shortcuts import render

# controllers = views = функции


def index(request):
    return render(request, 'products/index.html')


def products(request):
    return render(request, 'products/products.html')


def test_context(request):
    context = {
        'title': 'GeekShop',
        'header': 'Добро пожаловать на сайт!',
        'username': 'Иван Иванов',
    }
    return render(request, 'products/test_context.html', context)
