from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from milestones.models import Milestone
from resources.models import Resource


class ResourceTestCase(TestCase):
    def setUp(self):
        # Create a milestone object to be used for the resource
        self.milestone = Milestone.objects.create(
            name="Milestone 1",
            age=6,
            category=Milestone.SOCIAL,
            summary={"description": "Milestone summary"},
            is_current=True
        )

        # Initialize APIClient for making HTTP requests
        self.client = APIClient()

        # Create a resource object to use in GET/UPDATE/DELETE tests
        self.resource = Resource.objects.create(
            milestone=self.milestone,
            title="Social Development Article",
            tips={"tip1": "Be patient", "tip2": "Encourage interaction"},
            activities={"activity1": "Play with others", "activity2": "Watch facial expressions"},
            type="article"
        )

    def test_create_resource(self):
        """
        Test creating a new resource (happy path).
        """
        url = reverse('resource-list')
        data = {
            "milestone": self.milestone.milestone_id,  # Reference the milestone ID
            "title": "Cognitive Development Tutorial",
            "tips": {"tip1": "Encourage problem solving"},
            "activities": {"activity1": "Sort objects"},
            "type": "tutorial"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Resource created successfully.", response.data['message'])

    def test_create_resource_missing_field(self):
        """
        Test creating a new resource with missing fields (unhappy path).
        """
        url = reverse('resource-list')
        data = {
            "milestone": self.milestone.milestone_id,
            "title": "",  # Missing title
            "tips": {"tip1": "Encourage problem solving"},
            "activities": {"activity1": "Sort objects"},
            "type": "tutorial"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data['error'])  # Ensure the error for the missing title is returned

    def test_get_all_resources(self):
        """
        Test retrieving all resources (happy path).
        """
        url = reverse('resource-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # There should be one resource (created in setUp)

    def test_get_resource_by_id(self):
        """
        Test retrieving a single resource by ID (happy path).
        """
        url = reverse('resource-detail', args=[self.resource.resource_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.resource.title)

    def test_get_resource_by_id_not_found(self):
        """
        Test retrieving a non-existent resource (unhappy path).
        """
        url = reverse('resource-detail', args=[9999])  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_resource(self):
        """
        Test updating a resource (happy path).
        """
        url = reverse('resource-detail', args=[self.resource.resource_id])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Title")  # Ensure title was updated

    def test_delete_resource(self):
        """
        Test deleting a resource by ID (happy path).
        """
        url = reverse('resource-detail', args=[self.resource.resource_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_resource_by_activity(self):
        """
        Test searching for resources by activities (happy path).
        """
        url = reverse('resource-search')
        response = self.client.get(url, {'activities': 'Play with others'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # The activity should match one resource

    def test_search_resource_by_activity_not_found(self):
        """
        Test searching for resources by activities with no matching results (unhappy path).
        """
        url = reverse('resource-search')
        response = self.client.get(url, {'activities': 'Non-existent activity'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No resources should be found for this activity

    def test_search_resource_missing_activity_parameter(self):
        """
        Test searching for resources without providing the 'activities' parameter (unhappy path).
        """
        url = reverse('resource-search')
        response = self.client.get(url)  # No 'activities' parameter
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("activities parameter is required", response.data['error'])



