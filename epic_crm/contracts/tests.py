from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from .models import Contract
from users.models import CustomUser
from clients.models import Client
from rest_framework.authtoken.models import Token

class ContractManagementTestCase(TestCase):
    def setUp(self):
        Group.objects.create(name='Management')
        Group.objects.create(name='Sales')
        Group.objects.create(name='Support')

        self.management_user = CustomUser.objects.create_user(
            username='manager',
            password='testpass123',
            email='manager@example.com'
        )
        self.management_user.groups.add(Group.objects.get(name='Management'))

        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.management_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.test_client = Client.objects.create(
            full_name='Test Client',
            email='client@example.com',
            phone='1234567890',
            company_name='Test Company'
        )

    def test_management_can_create_contract(self):
        response = self.client.post('/api/contracts/contracts/', {
            'client': self.test_client.id,
            'total_amount': '1000.00',
            'amount_due': '500.00',
            'status': False
        })
        self.assertEqual(response.status_code, 201)

    def test_management_can_update_contract(self):
        contract = Contract.objects.create(
            client=self.test_client,
            total_amount='1000.00',
            amount_due='500.00',
            status=False
        )
        response = self.client.patch(f'/api/contracts/contracts/{contract.id}/', {
            'total_amount': '1100.00'
        })
        self.assertEqual(response.status_code, 200)

    def test_management_can_delete_contract(self):
        contract = Contract.objects.create(
            client=self.test_client,
            total_amount='1000.00',
            amount_due='500.00',
            status=False
        )
        response = self.client.delete(f'/api/contracts/contracts/{contract.id}/')
        self.assertEqual(response.status_code, 204)


class ContractSupportTestCase(TestCase):
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
        token, _ = Token.objects.get_or_create(user=self.support_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.test_client = Client.objects.create(
            full_name='Test Client',
            email='client@example.com',
            phone='1234567890',
            company_name='Test Company'
        )

        self.contract = Contract.objects.create(
            client=self.test_client,
            total_amount='1000.00',
            amount_due='500.00',
            status=False
        )

    def test_support_user_can_read_contract(self):
        response = self.client.get(f'/api/contracts/contracts/{self.contract.id}/')
        self.assertEqual(response.status_code, 200)

    def test_support_user_cannot_create_contract(self):
        response = self.client.post('/api/contracts/contracts/', {
            'client': self.test_client.id,
            'total_amount': '1000.00',
            'amount_due': '500.00',
            'status': False
        })
        self.assertEqual(response.status_code, 403)

    def test_support_user_cannot_update_contract(self):
        response = self.client.patch(f'/api/contracts/contracts/{self.contract.id}/', {
            'total_amount': '1100.00'
        })
        self.assertEqual(response.status_code, 403)

    def test_support_user_cannot_delete_contract(self):
        response = self.client.delete(f'/api/contracts/contracts/{self.contract.id}/')
        self.assertEqual(response.status_code, 403)