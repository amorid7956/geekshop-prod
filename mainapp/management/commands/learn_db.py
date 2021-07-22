from django.core.management import BaseCommand
from ...models import Product
from django.db.models import Q

class Command(BaseCommand):

    def handle(self, *args, **options):
        products_list = Product.objects.filter(
            Q(productcategory__name='�����') |  Q(productcategory__name='����������')
        )

        print(products_list, sep='\n')
