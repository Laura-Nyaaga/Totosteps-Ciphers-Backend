from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from milestones.models import Milestone
from child.models import Child
from api.serializers import MilestoneSerializer

# General setup for the test cases
class MilestoneTestCase(TestCase):
    def setUp(self):
        """
        Setup common test data for each test.
        """
        self.child = Child.objects.create(
            username='john_doe',  # Corrected field based on Child model
            date_of_birth='2020-01-01',  # Date of birth as per the Child model
            profile_picture=None,  # Optional field, can be left as None
            is_active=True  # Active child
        
        )
        
        # Create a milestone for testing
        self.milestone = Milestone.objects.create(
            name="Test Milestone",
            child_id=self.child,  # Ensure foreign key is correct
            age=6,  # Milestone for a 6-month-old child
            category=Milestone.SOCIAL,  # Choose one of the predefined categories
            summary={"description": "Test summary"},
            is_current=True
        )

        self.client = APIClient()

    # ------------------- Model Test Cases ---------------------
    def test_milestone_creation(self):
        """
        Test if milestone can be created successfully (happy path)
        """
        milestone = Milestone.objects.create(
            name="Another Milestone",
            child_id=self.child,
            age=12,
            category=Milestone.LANGUAGE,
            summary={"description": "Another summary"}
        )
        self.assertEqual(str(milestone), "Milestone at 12 months")

    def test_get_current_milestone(self):
        """
        Test getting the current milestone based on child's age (happy path)
        """
        current_milestone = Milestone.get_current_milestone(6)
        self.assertEqual(current_milestone, self.milestone)

    def test_get_current_milestone_no_match(self):
        """
        Test when there is no current milestone matching child's age (unhappy path)
        """
        current_milestone = Milestone.get_current_milestone(99)
        self.assertIsNone(current_milestone)

    # ------------------- Serializer Test Cases ---------------------
    def test_valid_milestone_serializer(self):
        """
        Test valid milestone serializer (happy path)
        """
        serializer = MilestoneSerializer(instance=self.milestone)
        self.assertEqual(serializer.data['name'], "Test Milestone")

    def test_invalid_milestone_serializer(self):
        """
        Test invalid milestone serializer (unhappy path)
        """
        invalid_data = {
            'name': '',
            'age': 99,  # Invalid age
            'category': 'Invalid',  # Invalid category
            'summary': {}
        }
        serializer = MilestoneSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('category', serializer.errors)

    # ------------------- View Test Cases ---------------------
    def test_get_milestone_list(self):
        """
        Test retrieving the list of milestones (happy path)
        """
        url = reverse('milestone-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_create_milestone(self):
    """
    Test creating a milestone (happy path)
    """
    url = reverse('milestone-list')
    data = {
        "name": "New Milestone",
        "child_id": self.child.child_id,  # Use child_id instead of id
        "age": 9,
        "category": Milestone.COGNITIVE,
        "summary": {"description": "Cognitive test"},
        "is_current": False
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)


def test_create_milestone_invalid(self):
    """
    Test creating a milestone with invalid data (unhappy path)
    """
    url = reverse('milestone-list')
    data = {
        "name": "",  # Invalid name
        "child_id": self.child.child_id,  # Use child_id instead of id
        "age": 99,  # Invalid age
        "category": "Invalid",  # Invalid category
        "summary": {}
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_get_milestone_detail(self):
        """
        Test retrieving a single milestone by ID (happy path)
        """
        url = reverse('milestone-detail', args=[self.milestone.milestone_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_milestone_detail_not_found(self):
        """
        Test retrieving a milestone with an invalid ID (unhappy path)
        """
        url = reverse('milestone-detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_milestone(self):
        """
        Test updating a milestone (happy path)
        """
        url = reverse('milestone-detail', args=[self.milestone.milestone_id])
        data = {"name": "Updated Milestone"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_milestone(self):
        """
        Test deleting a milestone (happy path)
        """
        url = reverse('milestone-detail', args=[self.milestone.milestone_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
