from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from milestones.models import Milestone
from result.models import Result
# from api.serializers import ResultSerializer


class ResultTestCase(TestCase):
    def setUp(self):
        # Create a milestone object
        self.milestone = Milestone.objects.create(
            name="Milestone 1",
            age=6,
            category=Milestone.SOCIAL,
            summary={"description": "Milestone summary"},
            is_current=True
        )

        # Initialize the APIClient for making HTTP requests
        self.client = APIClient()

        # Create a result object for testing GET and DELETE
        self.result = Result.objects.create(
            milestone=self.milestone,
            answers={"Q1": "Yes", "Q2": "No"},
            parent_email="testparent@example.com"
        )

    def test_create_result(self):
        """
        Test creating a new result (POST request).
        """
        url = reverse('create-result')
        data = {
            "milestone": self.milestone.milestone_id,  # Use milestone_id if that's the primary key
            "answers": {"Q1": "Yes", "Q2": "No"},
            "parent_email": "parent@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Result saved and email sent", response.data['detail'])

def test_create_result_missing_email(self):
    """
    Test creating a new result with missing parent email (POST request).
    """
    url = reverse('create-result')
    data = {
        "milestone": self.milestone.milestone_id,  # Use milestone_id if that's the primary key
        "answers": {"Q1": "Yes", "Q2": "No"},
        "parent_email": ""  # Missing email
    }
    response = self.client.post(url, data, format='json')

    # Check that the response returns 400 BAD REQUEST
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Adjusted error message check based on typical serializer validation error format
    self.assertIn('parent_email', response.data)  # Check if 'parent_email' error is present
    self.assertIn('This field may not be blank.', response.data['parent_email'])


    def test_get_all_results(self):
        """
        Test retrieving a list of all results (GET request).
        """
        url = reverse('create-result')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure only 1 result exists

    def test_get_result_by_id(self):
        """
        Test retrieving a specific result by ID (GET request).
        """
        url = reverse('get-result', args=[self.result.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['parent_email'], "testparent@example.com")

    def test_get_result_by_invalid_id(self):
        """
        Test retrieving a non-existent result by ID (unhappy path).
        """
        url = reverse('get-result', args=[9999])  # Invalid ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_result(self):
        """
        Test deleting a specific result by ID (DELETE request).
        """
        url = reverse('get-result', args=[self.result.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_result_invalid_id(self):
        """
        Test deleting a non-existent result by ID (unhappy path).
        """
        url = reverse('get-result', args=[9999])  # Invalid ID
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

