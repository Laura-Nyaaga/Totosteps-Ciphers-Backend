from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from child.models import Child
from users.models import User

class ChildAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parent = User.objects.create_user(
            email='parent@example.com',
            password='testpass',
            role='parent'
        )
        self.child = Child.objects.create(
            username='testchild',
            date_of_birth='2020-01-01',
            parent=self.parent
        )
    def test_child_list_happy_case(self):
        self.client.force_authenticate(user=self.parent)
        response = self.client.get(reverse('child-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testchild')
    def test_child_list_unauthenticated(self):
        response = self.client.get(reverse('child-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_child_create_happy_case(self):
        self.client.force_authenticate(user=self.parent)
        data = {
            'username': 'newchild',
            'date_of_birth': '2021-01-01',
        }
        response = self.client.post(reverse('child-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Child.objects.count(), 2)
    def test_child_create_invalid_data(self):
        self.client.force_authenticate(user=self.parent)
        data = {
            'username': '',
            'date_of_birth': '2021-01-01',
        }
        response = self.client.post(reverse('child-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_child_detail_happy_case(self):
        self.client.force_authenticate(user=self.parent)
        response = self.client.get(reverse('child-detail', args=[self.child.child_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testchild')
    def test_child_detail_unauthenticated(self):
        response = self.client.get(reverse('child-detail', args=[self.child.child_id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_child_delete_happy_case(self):
        self.client.force_authenticate(user=self.parent)
        response = self.client.delete(reverse('child-detail', args=[self.child.child_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.child.refresh_from_db()
        self.assertFalse(self.child.is_active)
    def test_child_delete_unauthenticated(self):
        response = self.client.delete(reverse('child-detail', args=[self.child.child_id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)