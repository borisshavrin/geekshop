from django.contrib.auth.mixins import LoginRequiredMixin
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, RedirectView, UpdateView, DetailView, DeleteView
from django.views.generic.detail import DetailView

from basket.models import Basket
from orders.forms import OrderItemForm
from orders.models import Order, OrderItem
from products.models import Product


class OrderListView(ListView):
    model = Order
    template_name = 'orders/orders.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    context_object_name = 'object'
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        context = super(OrderItemsCreateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                     form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price

                basket_items.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreateView, self).form_valid(form)


class OrderItemsUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = []
    context_object_name = 'object'
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        context = super(OrderItemsUpdateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsUpdateView, self).form_valid(form)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:orders_list')



class OrderReadView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderReadView, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('orders:orders_list'))


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=int(pk)).first()

        if product:
            return JsonResponse({'price': product.price})
        else:
            return JsonResponse({'price': 0})

@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    """ Изменение остатков товаров на складе при добавлении товаров в корзину или заказ
        «sender» - класс отправителя;
        «update_fields» - имена обновляемых полей;
        «instance» - сам обновляемый объект """
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            """Если объект не сохранен"""
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    """ Изменение остатков товаров на складе при добавлении товаров в корзину или заказ """
    instance.product.quantity += instance.quantity
    instance.product.save()
