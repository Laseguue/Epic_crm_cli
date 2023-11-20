from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from .models import CustomUser
from rest_framework.authtoken.models import Token


class UserTestCase(TestCase):
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

        self.token, _ = Token.objects.get_or_create(user=self.management_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_user(self):
        self.client.login(username='manager', password='testpass123')
        response = self.client.post('/api/users/users/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'groups': ['Sales']
        })
        self.assertEqual(response.status_code, 201)
        new_user = CustomUser.objects.get(username='newuser')
        self.new_user_id = new_user.id

    def test_list_users(self):
        self.client.login(username='manager', password='testpass123')
        response = self.client.get('/api/users/users/')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        user_to_update = CustomUser.objects.create_user(
            username='updatableuser',
            email='updatable@example.com',
            password='testpass'
        )
        self.client.login(username='manager', password='testpass123')
        response = self.client.patch(f'/api/users/users/{user_to_update.id}/', {
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        user_to_delete = CustomUser.objects.create_user(
            username='deletableuser',
            email='deletable@example.com',
            password='testpass'
        )
        self.client.login(username='manager', password='testpass123')
        response = self.client.delete(f'/api/users/users/{user_to_delete.id}/')
        self.assertEqual(response.status_code, 204)

class UserPermissionTestCase(TestCase):
    def setUp(self):
        Group.objects.create(name='Management')
        Group.objects.create(name='Sales')
        Group.objects.create(name='Support')

        self.support_user = CustomUser.objects.create_user(
            username='supportuser',
            password='supportpass',
            email='supportuser@example.com'
        )
        support_group = Group.objects.get(name='Support')
        self.support_user.groups.add(support_group)
        support_token, _ = Token.objects.get_or_create(user=self.support_user)

        self.support_client = APIClient()
        self.support_client.credentials(HTTP_AUTHORIZATION='Token ' + support_token.key)
    
    def test_create_user(self):
        self.support_client.login(username='supportuser', password='supportpass')
        response = self.support_client.post('/api/users/users/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'groups': ['Sales']
        })
        self.assertEqual(response.status_code, 403)

    def test_list_users(self):
        self.support_client.login(username='supportuser', password='supportpass')
        response = self.support_client.get('/api/users/users/')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        user_to_update = CustomUser.objects.create_user(
            username='updatableuser',
            email='updatable@example.com',
            password='testpass'
        )
        self.support_client.login(username='supportuser', password='supportpass')
        response = self.support_client.patch(f'/api/users/users/{user_to_update.id}/', {
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_user(self):
        user_to_delete = CustomUser.objects.create_user(
            username='deletableuser',
            email='deletable@example.com',
            password='testpass'
        )
        self.support_client.login(username='supportuser', password='supportpass')
        response = self.support_client.delete(f'/api/users/users/{user_to_delete.id}/')
        self.assertEqual(response.status_code, 403)