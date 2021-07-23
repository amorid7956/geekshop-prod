from django.core.management import BaseCommand
from ...models import Product
from django.db.models import Q, F, When, Case, IntegerField, DecimalField
from datetime import timedelta
from ordersapp.models import OrderItem

class Command(BaseCommand):

    def handle(self, *args, **options):
        action_1 = 1
        action_2 = 2
        action_3 = 3

        action_1_timedelta = timedelta(hours=12)
        action_2_timedelta = timedelta(hours=24)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.05

        action_1_condition = Q(order__updated_at__lte=F('order__created_at') + action_1_timedelta)
        action_2_condition = Q(order__updated_at__gt=F('order__created_at') + action_1_timedelta) & \
                             Q(order__updated_at__lte=F('order__created_at') + action_2_timedelta)
        action_3_condition = Q(order__updated_at__gt=F('order__created_at') + action_2_timedelta)

        action_1_order = When(action_1_condition, then=action_1)
        action_2_order = When(action_2_condition, then=action_2)
        action_3_order = When(action_3_condition, then=action_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('product__quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('product__quantity') * action_2_discount)
        action_3_price = When(action_3_condition, then=F('product__price') * F('product__quantity') * action_3_discount)

        orders_items = OrderItem.objects.annotate(
            action_order = Case(
                action_1_order,
                action_2_order,
                action_3_order,
                output_field=IntegerField()
            )
        ).annotate(
            total_price = Case(
                action_1_price,
                action_2_price,
                action_3_price,
                output_field=DecimalField()
            )
        ).order_by('action_order', 'total_price').select_related()

        for item in orders_items:
            print(f'{item.action_order} order#{item.pk} {item.product.name} '
                  f'discount: {abs(item.total_price):6.2f} || {item.order.updated_at - item.order.created_at}')
        # products_list = Product.objects.filter(
        #     Q(category__name='Обувь') |  Q(category__name='Аксессуары')
        # )
        # print(products_list, sep='\n')
