from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from child.models import Child

User = get_user_model()

class ChildAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.parent = User.objects.create_user(
            email='parent@example.com',
            password='testpass',
            role='parent'
        )

        self.another_parent = User.objects.create_user(
            email='another_parent@example.com',
            password='testpass',
            role='parent'
        )

        self.client.force_authenticate(user=self.parent)
        self.child = Child.objects.create(
            username='testchild',
            date_of_birth='2021-01-01',
            parent=self.parent
        )

    def test_create_child_happy_case(self):
        data = {
            'username': 'newchild',
            'date_of_birth': '2022-01-01',
            'parent': self.parent.user_id
        }

        response = self.client.post(reverse('child-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Child.objects.count(), 2)
        created_child = Child.objects.get(username='newchild')
        self.assertEqual(created_child.username, 'newchild')
        self.assertEqual(created_child.parent, self.parent)

    def test_create_child_missing_data(self):
        data = {
            'username': '',  
            'date_of_birth': '2022-01-01'
        }

        response = self.client.post(reverse('child-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_child_list_happy_case(self):
        response = self.client.get(reverse('child-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testchild')

    def test_get_child_detail_happy_case(self):
        response = self.client.get(reverse('child-detail', args=[self.child.child_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testchild')
        self.assertEqual(response.data['parent'], self.parent.user_id)
        
    def test_delete_child_happy_case(self):
        response = self.client.delete(reverse('child-detail', args=[self.child.child_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.child.refresh_from_db()
        self.assertFalse(self.child.is_active)

   
