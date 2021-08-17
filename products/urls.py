from django.urls import path
from django.views.decorators.cache import cache_page

from products.views import products, products_ajax

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('<int:category_id>/', products, name='category'),
    path('<int:category_id>/ajax', cache_page(3600)(products_ajax)),
    path('page/<int:page>', products, name='page'),
    path('page/<int:page>/ajax', cache_page(3600)(products_ajax)),
]
