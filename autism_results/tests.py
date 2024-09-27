
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from autism_image.models import Autism_Image
from autism_results.models import Autism_Results
from child.models import Child
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
import io
from PIL import Image
class AutismResultTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a parent user
        self.parent_user = User.objects.create_user(
            email='parent@example.com',
            password='testpassword',
            role='parent'
        )
        
        self.child = Child.objects.create(
            username="test_child",
            date_of_birth=date(2010, 1, 1),
            parent=self.parent_user
        )
        
        image_content = io.BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(image_content, format='JPEG')
        image_content.seek(0)
        self.autism_image = Autism_Image.objects.create(
            child=self.child,
            image_upload=SimpleUploadedFile('test_image.jpg', image_content.read(), content_type='image/jpeg')
        )
        # Create a autism result related to the autism image
        self.autism_result = Autism_Results.objects.create(
            image=self.autism_image,
            result="Positive"
        )
        
        # URLs for list and detail views
        self.list_url = reverse('autism-result-list')
    # Test GET request for Autism Results
    def test_get_autism_results_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 
        self.assertEqual(response.data[0]['result'], 'Positive')
        
    # Happy Test Case: Test POST request for Autism Results
    def test_post_autism_result(self):
        data = {
            "image": self.autism_image.image_id,
            "result": "Negative"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['result'], "Negative")

    # Unhappy Test Case: Test POST request with missing result field
    def test_post_autism_result_invalid(self):
        data = {
            "image": self.autism_image.image_id  
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('result', response.data)  

    # Unhappy Test Case: Test POST request with invalid image_id
    def test_post_autism_result_invalid_image(self):
        data = {
            "image": 999,  
            "result": "Negative"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('image', response.data)  

