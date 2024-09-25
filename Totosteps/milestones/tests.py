from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from milestones.models import Milestone
from child.models import Child
from django.contrib.auth import get_user_model 
from datetime import date


class MilestoneTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Get the custom user model
        User = get_user_model()

        # Create a test user and child
        self.user = User.objects.create_user(
            email='parent@example.com',  # Pass the email argument
            password='password123',
            role='parent'  # Pass the role argument
        )
        self.child = Child.objects.create(
            username='child1',
            date_of_birth=date(2022, 1, 1),
            parent=self.user
        )

        # Create some test milestones
        self.milestone1 = Milestone.objects.create(
            name="Social Smile",
            child_id=self.child,
            age=2,
            category=Milestone.SOCIAL,
            summary={"description": "Smiles at people"},
            is_current=True
        )
        self.milestone2 = Milestone.objects.create(
            name="Babbles",
            child_id=self.child,
            age=4,
            category=Milestone.LANGUAGE,
            summary={"description": "Begins to babble"},
            is_current=True
        )


    def test_get_all_milestones(self):
        url = reverse('milestone-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_milestone(self):
        url = reverse('milestone-detail', args=[self.milestone1.milestone_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.milestone1.name)

    def test_get_single_milestone_not_found(self):
        url = reverse('milestone-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_milestone(self):
        url = reverse('milestone-list')
        data = {
            "name": "Sits without support",
            "child_id": self.child.child_id,
            "age": 6,
            "category": Milestone.MOVEMENT,
            "summary": {"description": "Can sit without support"},
            "is_current": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Sits without support")

    def test_create_milestone_invalid_data(self):
        url = reverse('milestone-list')
        data = {
            "name": "",  # Invalid: name is required
            "child_id": self.child.child_id,
            "age": 6,
            "category": Milestone.MOVEMENT,
            "summary": {"description": "Can sit without support"},
            "is_current": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_milestone(self):
        url = reverse('milestone-detail', args=[self.milestone1.milestone_id])
        data = {
            "name": "Smiles at everyone",
            "is_current": False
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Smiles at everyone")
        self.assertEqual(response.data['is_current'], False)

    def test_update_milestone_invalid_data(self):
        url = reverse('milestone-detail', args=[self.milestone1.milestone_id])
        data = {
            "age": "invalid"  # Invalid: age must be an integer
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_milestone(self):
        url = reverse('milestone-detail', args=[self.milestone1.milestone_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Milestone.objects.filter(milestone_id=self.milestone1.milestone_id).exists())

    def test_delete_milestone_not_found(self):
        url = reverse('milestone-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_child_milestones(self):
        url = reverse('child_milestones', args=[self.child.child_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertFalse(any(m['is_current'] for m in response.data))

    def test_get_child_milestones_child_not_found(self):
        url = reverse('child_milestones', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
