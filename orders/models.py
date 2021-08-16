from django.conf import settings
from django.db import models

from products.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'Формируется'),
        (SENT_TO_PROCEED, 'Отправлен в обработку'),
        (PAID, 'Оплачен'),
        (PROCEEDED, 'Обрабатывается'),
        (READY, 'Готов к выдаче'),
        (CANCEL, 'Отменен'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True,
    )

    update = models.DateTimeField(
        verbose_name='Обновлен',
        auto_now=True,
    )

    status = models.CharField(
        verbose_name='Статус',
        max_length=3,
        choices=ORDER_STATUS_CHOICES,
        default=FORMING,
    )

    is_active = models.BooleanField(
        verbose_name='Активен',
        default=True,
    )

    class Meta:
        ordering = ('-created',)            # сортировка по умолчанию от более новых к старым заказам
        verbose_name = 'Заказ'              # имя класса в единственном числе
        verbose_name_plural = 'Заказы'      # имя класса во множественном числе


    def __str__(self):
        return f'Тукущий заказ {self.id}'

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }

    def get_product_quantity(self):
        items = self.orderitems.select_related()        # Выбрать все связанные объекты
        return len(items)

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="orderitems",
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=0,
    )

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()

    def get_product_cost(self):
        return self.product.price * self.quantity


