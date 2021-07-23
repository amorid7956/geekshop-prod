from django.test import TestCase
from authapp.models import User
from django.test.client import Client

class UserManagementTestCase(TestCase):
    username = 'django'
    email='test@email.ru'
    password = 'testpass'
    status_code_success = 200
    status_code_redirect = 302

    def setUp(self):
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    def test_login(self):
        response = self.client.get('/main/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, self.status_code_redirect)