from django.urls import path

from .views import OrderListView, OrderItemsCreateView, order_forming_complete, OrderReadView,\
    OrderItemsUpdateView, OrderDeleteView, get_product_price


app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list'),
    path('forming/complete/<int:pk>/', order_forming_complete, name='order_forming_complete'),
    path('create/', OrderItemsCreateView.as_view(), name='order_create'),
    path('read/<int:pk>/', OrderReadView.as_view(), name='order_read'),
    path('update/<int:pk>/', OrderItemsUpdateView.as_view(), name='order_update'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('product/<int:pk>/price/', get_product_price),
]
