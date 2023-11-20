from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from .models import Event
from contracts.models import Contract
from users.models import CustomUser
from clients.models import Client
from rest_framework.authtoken.models import Token

class EventSalesTestCase(TestCase):
    def setUp(self):
        Group.objects.create(name='Management')
        Group.objects.create(name='Sales')
        Group.objects.create(name='Support')

        self.sales_user = CustomUser.objects.create_user(
            username='salesperson',
            password='testpass123',
            email='sales@example.com'
        )
        self.sales_user.groups.add(Group.objects.get(name='Sales'))

        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.sales_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.test_client = Client.objects.create(
            full_name='Test Client Sales',
            email='client.sales@example.com',
            phone='9876543210',
            company_name='Sales Company'
        )
        self.contract = Contract.objects.create(
            client=self.test_client,
            total_amount='2000.00',
            amount_due='1000.00',
            status=True,
            sales_contact=self.sales_user
        )

    def test_sales_user_can_create_event(self):
        response = self.client.post('/api/events/events/', {
            'contract': self.contract.id,
            'event_start_date': '2023-12-01T10:00:00Z',
            'event_end_date': '2023-12-01T18:00:00Z',
            'location': 'Downtown Conference Center',
            'attendees': 100,
            'notes': 'Annual Sales Meeting'
        })
        self.assertEqual(response.status_code, 201)

    def test_sales_user_cannot_update_event(self):
        event = Event.objects.create(
            contract=self.contract,
            support_contact=None,
            event_start_date='2023-12-01T10:00:00Z',
            event_end_date='2023-12-01T18:00:00Z',
            location='Downtown Conference Center',
            attendees=100,
            notes='Annual Sales Meeting'
        )
        response = self.client.patch(f'/api/events/events/{event.id}/', {
            'location': 'New Location'
        })
        self.assertEqual(response.status_code, 403)

class EventSupportTestCase(TestCase):
    def setUp(self):
        Group.objects.create(name='Management')
        Group.objects.create(name='Sales')
        Group.objects.create(name='Support')

        self.support_user = CustomUser.objects.create_user(
            username='supportperson',
            password='testpass123',
            email='support@example.com'
        )
        self.support_user.groups.add(Group.objects.get(name='Support'))

        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.support_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.test_client = Client.objects.create(
            full_name='Test Client Support',
            email='client.support@example.com',
            phone='1234567890',
            company_name='Support Company'
        )
        self.contract = Contract.objects.create(
            client=self.test_client,
            total_amount='1500.00',
            amount_due='750.00',
            status=True
        )

    def test_support_user_can_update_event(self):
        event = Event.objects.create(
            contract=self.contract,
            support_contact=self.support_user,
            event_start_date='2023-11-01T09:00:00Z',
            event_end_date='2023-11-01T17:00:00Z',
            location='Support Venue',
            attendees=50,
            notes='Support Team Meeting'
        )
        response = self.client.patch(f'/api/events/events/{event.id}/', {
            'attendees': 60
        })
        self.assertEqual(response.status_code, 200)

    def test_support_user_cannot_create_event(self):
        response = self.client.post('/api/events/events/', {
            'contract': self.contract.id,
            'support_contact': self.support_user.id,
            'event_start_date': '2023-11-01T09:00:00Z',
            'event_end_date': '2023-11-01T17:00:00Z',
            'location': 'Support Venue',
            'attendees': 50,
            'notes': 'Attempt to Create Event'
        })
        self.assertEqual(response.status_code, 403)

class EventManagementTestCase(TestCase):
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
            full_name='Test Client Management',
            email='client.management@example.com',
            phone='3216549870',
            company_name='Management Company'
        )
        self.contract = Contract.objects.create(
            client=self.test_client,
            total_amount='3000.00',
            amount_due='1500.00',
            status=True
        )

    def test_management_user_can_delete_event(self):
        event = Event.objects.create(
            contract=self.contract,
            support_contact=None,
            event_start_date='2024-01-01T10:00:00Z',
            event_end_date='2024-01-01T18:00:00Z',
            location='Management Conference Room',
            attendees=200,
            notes='Management Annual Review'
        )
        response = self.client.delete(f'/api/events/events/{event.id}/')
        self.assertEqual(response.status_code, 204)
