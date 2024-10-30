
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from result.models import Result
from milestones.models import Milestone
from child.models import Child
from users.models import User
from assessment.models import Assessment

class ResultAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass',
            role='parent'
        )
        self.child = Child.objects.create(
            username='testchild',
            date_of_birth='2020-01-01',
            parent=self.user
        )
        self.milestone = Milestone.objects.create(
         name="Social Smile",
            age=2,
            description="Milestone summary",
            summary={"description": "Smiles at people"},
            image = SimpleUploadedFile(
            name='test_image.jpeg',
            content=b'\x47\x49\x46\x38\x39\x61',  
            content_type='image/jpeg'
        )
        )
        self.assessment = Assessment.objects.create(
            milestone=self.milestone,
            question={'question': 'Test question'},
            correct_answer='YES',
            question_type='multiple choice',
            category='Social'
        )
    def test_create_result_valid_data(self):
        url = reverse('create-result')
        data = {
            'milestone': self.milestone.milestone_id,
            'user': self.user.user_id,
            'answers': {'question1': 'YES', 'question2': 'NO'}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Result.objects.count(), 1)
    def test_create_result_invalid_data(self): 
        url = reverse('create-result') 
        data = {        
            'milestone': self.milestone.milestone_id, 
            'user': self.user.user_id,        
            'answers': ''    } 
        response = self.client.post(url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def test_get_result_list(self):
        url = reverse('create-result')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    def test_get_specific_result(self):
        result = Result.objects.create(
            milestone=self.milestone,
            user=self.user,
            answers={'question1': 'YES', 'question2': 'NO'}
        )
        url = reverse('get-result', args=[result.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], result.id)
    def test_delete_specific_result(self):
        result = Result.objects.create(
            milestone=self.milestone,
            user=self.user,
            answers={'question1': 'YES', 'question2': 'NO'}
        )
        url = reverse('get-result', args=[result.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Result.objects.count(), 0)




