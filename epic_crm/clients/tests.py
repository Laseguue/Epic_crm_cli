from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from .models import Client
from users.models import CustomUser
from rest_framework.authtoken.models import Token

class ClientTestCase(TestCase):
    def setUp(self):
        Group.objects.create(name='Management')
        Group.objects.create(name='Sales')
        Group.objects.create(name='Support')

        self.sales_user = CustomUser.objects.create_user(
            username='sales',
            password='testpass123',
            email='sales@example.com'
        )
        self.sales_user.groups.add(Group.objects.get(name='Sales'))

        self.client = APIClient()

        self.token, _ = Token.objects.get_or_create(user=self.sales_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_create_client(self):
        response = self.client.post('/api/clients/clients/', {
            'full_name': 'newclient',
            'email': 'newclient@example.com',
            'phone': '1234567890',
            'company_name': 'test'
        })
        self.assertEqual(response.status_code, 201)

    def test_list_clients(self):
        response = self.client.get('/api/clients/clients/')
        self.assertEqual(response.status_code, 200)

    def test_update_client(self):
        client_to_update = Client.objects.create(
            full_name='Unowned Client',
            email='unowned@example.com',
            phone='0987654321',
            company_name='Unowned Company',
            sales_contact= self.sales_user
        )
        response = self.client.patch(f'/api/clients/clients/{client_to_update.id}/', {
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_client(self):
        client_to_delete = Client.objects.create(
            full_name='Unowned Client',
            email='unowned@example.com',
            phone='0987654321',
            company_name='Unowned Company',
            sales_contact= self.sales_user
        )
        response = self.client.delete(f'/api/clients/clients/{client_to_delete.id}/')
        self.assertEqual(response.status_code, 204)


class ClientPermissionTestCase(TestCase):
    def setUp(self):
        Group.objects.create(name='Management')
        Group.objects.create(name='Sales')
        Group.objects.create(name='Support')

        self.support_user = CustomUser.objects.create_user(
            username='support',
            password='testpass123',
            email='support@example.com'
        )
        self.support_user.groups.add(Group.objects.get(name='Support'))

        self.client = APIClient()

        self.token, _ = Token.objects.get_or_create(user=self.support_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_support_user_cannot_create_client(self):
        response = self.client.post('/api/clients/clients/', {
            'full_name': 'newclient',
            'email': 'newclient@example.com',
            'phone': '1234567890',
            'company_name': 'test'
        })
        self.assertEqual(response.status_code, 403)

    def test_support_user_cannot_update_client(self):
        client = Client.objects.create(
            full_name='Existing Client',
            email='existing@example.com',
            phone='1234567890',
            company_name='Existing Company',
        )
        response = self.client.patch(f'/api/clients/clients/{client.id}/', {
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 403)

    def test_support_user_list_client(self):
        response = self.client.get('/api/users/users/')
        self.assertEqual(response.status_code, 200)

    def test_support_user_cannot_delete_client(self):
        client = Client.objects.create(
            full_name='Existing Client',
            email='existing@example.com',
            phone='1234567890',
            company_name='Existing Company',
        )
        response = self.client.delete(f'/api/clients/clients/{client.id}/')
        self.assertEqual(response.status_code, 403)