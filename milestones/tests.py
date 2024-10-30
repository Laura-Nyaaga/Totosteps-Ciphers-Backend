from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from milestones.models import Milestone
from datetime import date
import json

class MilestoneTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

       
        self.milestone1 = Milestone.objects.create(
            name="Social Smile",
            age=2,
            description="Milestone summary",
            summary={"description": "Smiles at people"},
            image = SimpleUploadedFile(
            name='test_image.jpeg',
            content=b'\x47\x49\x46\x38\x39\x61',  # Minimal valid GIF header content
            content_type='image/jpeg'
        )
        )
        self.milestone2 = Milestone.objects.create(
            name="Babbles",
            age=4,
            description="Milestone Babbles",
            summary={"description": "Begins to babble"},
            image = SimpleUploadedFile(
            name='testone_image.png',
            content=b'\x46\x48\x47\x39\x38\x60',  # Minimal valid GIF header content
            content_type='image/png'
        )
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

    def test_create_milestone_invalid_data(self):
        url = reverse('milestone-list')
        data = {
            "name": "",  
            "age": 6,
            "summary": {"description": "Can sit without support"},
            "image": SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',              
            content_type='image/jpeg'
        )
          
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_milestone(self):
        url = reverse('milestone-detail', args=[self.milestone1.milestone_id])
        data = {
            "name": "Smiles at everyone",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Smiles at everyone")

    def test_update_milestone_invalid_data(self):
        url = reverse('milestone-detail', args=[self.milestone1.milestone_id])
        data = {
            "age": "invalid"  
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

    