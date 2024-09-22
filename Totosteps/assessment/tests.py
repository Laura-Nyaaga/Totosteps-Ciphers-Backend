from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from milestones.models import Milestone
from assessment.models import Assessment
from api.serializers import AssessmentSerializer

class AssessmentTestCase(TestCase):
    def setUp(self):
        """
        Setup common test data for all test cases.
        """
        # Create a milestone for testing
        self.milestone = Milestone.objects.create(
            name="Milestone 1",
            age=6,
            category=Milestone.SOCIAL,
            summary={"description": "Milestone summary"},
            is_current=True
        )
        
        # Create an assessment question for testing
        self.assessment = Assessment.objects.create(
            milestone=self.milestone,
            question="Is the child social at 6 months?",
            correct_answer="YES",
            question_type="multiple choice",
            category=Assessment.SOCIAL
        )

        self.client = APIClient()

    # ------------------- Model Test Cases ---------------------
    def test_assessment_creation(self):
        """
        Test creating an assessment (happy path).
        """
        assessment = Assessment.objects.create(
            milestone=self.milestone,
            question="Is the child moving?",
            correct_answer="YES",
            question_type="multiple choice",
            category=Assessment.MOVEMENT
        )
        self.assertEqual(str(assessment), f"{assessment.question_id} Is the child moving?")
    
    def test_unique_question(self):
        """
        Test that duplicate questions cannot be created (unhappy path).
        """
        with self.assertRaises(Exception):  # IntegrityError expected
            Assessment.objects.create(
                milestone=self.milestone,
                question="Is the child social at 6 months?",  # Duplicate question
                correct_answer="YES",
                question_type="multiple choice",
                category=Assessment.SOCIAL
            )

    # ------------------- Serializer Test Cases ---------------------
    def test_valid_assessment_serializer(self):
        """
        Test valid assessment serializer (happy path).
        """
        serializer = AssessmentSerializer(instance=self.assessment)
        self.assertEqual(serializer.data['question'], "Is the child social at 6 months?")

    def test_invalid_assessment_serializer(self):
        """
        Test invalid assessment serializer (unhappy path).
        """
        invalid_data = {
            'milestone': None,  # Missing required field
            'question': '',  # Empty question (invalid)
            'correct_answer': 'YES',
            'question_type': 'multiple choice',
            'category': Assessment.SOCIAL
        }
        serializer = AssessmentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('question', serializer.errors)

    # ------------------- View Test Cases ---------------------
    def test_get_all_assessments(self):
        """
        Test retrieving all assessment questions (happy path).
        """
        url = reverse('list_all_questions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_assessment(self):
        """
        Test creating an assessment question (happy path).
        """
        url = reverse('assessment_create')
        data = {
            "milestone": self.milestone.milestone_id,
            "question": "Can the child recognize objects?",
            "correct_answer": "YES",
            "question_type": "multiple choice",
            "category": Assessment.COGNITIVE
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_assessment_invalid(self):
        """
        Test creating an assessment question with invalid data (unhappy path).
        """
        url = reverse('assessment_create')
        data = {
            "milestone": "",  # Invalid milestone
            "question": "",  # Empty question
            "correct_answer": "YES",
            "question_type": "multiple choice",
            "category": Assessment.COGNITIVE
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_assessment_detail(self):
        """
        Test retrieving a single assessment question by ID (happy path).
        """
        url = reverse('get_question_by_id', args=[self.assessment.question_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_assessment_detail_not_found(self):
        """
        Test retrieving a non-existent assessment question by ID (unhappy path).
        """
        url = reverse('get_question_by_id', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_assessment(self):
        """
        Test updating an assessment question (happy path).
        """
        url = reverse('get_question_by_id', args=[self.assessment.question_id])
        data = {"question": "Updated question"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_assessment(self):
        """
        Test deleting an assessment question (happy path).
        """
        url = reverse('get_question_by_id', args=[self.assessment.question_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_category_questions(self):
        """
        Test listing questions by category (happy path).
        """
        url = reverse('category-questions-list', args=[Assessment.SOCIAL])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_category_questions_not_found(self):
        """
        Test listing questions by category where no questions exist (unhappy path).
        """
        url = reverse('category-questions-list', args=["Unknown"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
