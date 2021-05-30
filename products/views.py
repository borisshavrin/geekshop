from django.shortcuts import render

# controllers = views = функции


def index(request):
    return render(request, 'products/index.html')


def products(request):
    return render(request, 'products/products.html')
