from django.test import TestCase
from authapp.models import User
from django.test.client import Client
from django.conf import settings

class UserManagementTestCase(TestCase):
    username = 'django'
    email='test@email.ru'
    password = 'testpass'
    status_code_success = 200
    status_code_redirect = 302

    new_user_data = {
        'username' : 'django1',
        'first_name' : 'django',
        'last_name' : 'django',
        'password1' : 'geekbrains',
        'password2' : 'geekbrains',
        'age' : 24,
        'email' : 'test@email.ru'
    }
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

    def test_user_register(self):
        response = self.client.post('/users/register/', data=self.new_user_data)
        self.assertEqual(response.status_code, self.status_code_redirect)

        new_user = User.objects.get(username=self.new_user_data['username'])
        activation_url = f'{settings.DOMAIN_NAME}/users/verify/{new_user.email}/{new_user.activation_key}/'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)

    def test_user_logout(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
