from django.core.management import BaseCommand
from ...models import Product
from django.db.models import Q

class Command(BaseCommand):

    def handle(self, *args, **options):
        products_list = Product.objects.filter(
            Q(category__name='Обувь') |  Q(category__name='Аксессуары')
        )

        print(products_list, sep='\n')
