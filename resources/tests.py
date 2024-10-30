from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from resources.models import Resource

class ResourceTestCase(TestCase):
    def setUp(self):
        
        self.client = APIClient()

        self.resource = Resource.objects.create(
            title="Social Development Article",
            tips={"tip1": "Be patient", "tip2": "Encourage interaction"},
            activities={"activity1": "Play with others", "activity2": "Watch facial expressions"},
            image=None
        )

    def test_create_resource(self):
        url = reverse('resource-list')
        data = {
            "title": "Cognitive Development Tutorial",
            "tips": {"tip1": "Encourage problem solving"},
            "activities": {"activity1": "Sort objects"},
            "image": None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Resource created successfully.", response.data['message'])

    def test_create_resource_missing_field(self):
        url = reverse('resource-list')
        data = {
            "title": "", 
            "tips": {"tip1": "Encourage problem solving"},
            "activities": {"activity1": "Sort objects"},
            "image": None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data['error'])  

    def test_get_all_resources(self):
        url = reverse('resource-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  

    def test_get_resource_by_id(self):
        url = reverse('resource-detail', args=[self.resource.resource_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.resource.title)

    def test_get_resource_by_id_not_found(self):
        url = reverse('resource-detail', args=[9999])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_resource(self):
        url = reverse('resource-detail', args=[self.resource.resource_id])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Title")  

    def test_delete_resource(self):
        url = reverse('resource-detail', args=[self.resource.resource_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_resource_by_activity(self):
        url = reverse('resource-search')
        response = self.client.get(url, {'activities': 'Play with others'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  

    def test_search_resource_by_activity_not_found(self):
        url = reverse('resource-search')
        response = self.client.get(url, {'activities': 'Non-existent activity'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  

    def test_search_resource_missing_activity_parameter(self):
        url = reverse('resource-search')
        response = self.client.get(url)  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("activities parameter is required", response.data['error'])
