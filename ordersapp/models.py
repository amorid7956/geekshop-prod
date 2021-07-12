from django.db import models
from django.conf import settings
from mainapp.models import Product

class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED ='PRD'
    PAID = 'PD'
    READY = 'RD'
    CANCEL = 'CNC'
    DELIVERED = 'DVD'

    STATUSES = (
        (FORMING, 'Формируется'),
        (SENT_TO_PROCEED, 'Отправлен в обработку'),
        (PROCEEDED, 'Обработан'),
        (PAID, 'Оплачен'),
        (READY, 'Готов к выдаче'),
        (CANCEL, 'Отменён'),
        (DELIVERED, 'Выдан'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Обновлён')
    status = models.CharField(choices=STATUSES, default=FORMING,verbose_name='Статус', max_length=3)
    is_active = models.BooleanField(default=True)

    def get_total_quantity(self):
        _items = self.orderitems.select_related()
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    def get_total_cost(self):
        _items = self.orderitems.select_related()
        _totalcost = sum(list(map(lambda x: x.get_product_cost(), _items)))
        return _totalcost

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.save()
        self.is_active = False
        self.save()

    @staticmethod
    def get_item(pk):
        return Order.objects.get(pk=pk)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    def get_product_cost(self):
        return self.product.price * self.quantity


