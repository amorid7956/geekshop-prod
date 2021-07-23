from django.test import TestCase
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket
from authapp.models import User

class BasketTestCase(TestCase):
    username = 'django'
    email='test@email.ru'
    password = 'testpass'

    def setUp(self):
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        category = ProductCategory.objects.create(name="стулья")
        self.product_1 = Product.objects.create(name="стул 1",
                                          category=category,
                                          price = 1999,
                                          quantity=150)

        self.product_2 = Product.objects.create(name="стул 2",
                                          category=category,
                                          price=2998,
                                          quantity=125)

        self.product_3 = Product.objects.create(name="стул 3",
                                          category=category,
                                          price=998,
                                          quantity=115)

        self.basket_1 = Basket.objects.create(user=self.user,
                                          product=self.product_1,
                                          quantity=2)

        self.basket_2 = Basket.objects.create(user=self.user,
                                          product=self.product_2,
                                          quantity=3)

        self.basket_3 = Basket.objects.create(user=self.user,
                                          product=self.product_3,
                                          quantity=4)


    def test_basket_get(self):
        basket_1 = Basket.objects.get(user=self.user,product=self.product_1)
        basket_2 = Basket.objects.get(user=self.user,product=self.product_2)
        basket_3 = Basket.objects.get(user=self.user,product=self.product_3)
        self.assertEqual(basket_1, self.basket_1)
        self.assertEqual(basket_2, self.basket_2)
        self.assertEqual(basket_3, self.basket_3)

    def test_basket_sum(self):
        basket_1 = Basket.objects.get(user=self.user,product=self.product_1)
        basket_2 = Basket.objects.get(user=self.user,product=self.product_2)
        basket_3 = Basket.objects.get(user=self.user,product=self.product_3)
        sum_1 = basket_1.quantity * basket_1.product.price
        sum_2 = basket_2.quantity * basket_2.product.price
        sum_3 = basket_3.quantity * basket_3.product.price
        self.assertEqual(basket_1.sum(), sum_1)
        self.assertEqual(basket_2.sum(), sum_2)
        self.assertEqual(basket_3.sum(), sum_3)
