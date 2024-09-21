from django.test import TestCase
from autism_image.models import Autism_Image
from django.utils import timezone
from autism_results.models import Autism_Results
from django.db import IntegrityError


class AutismResultsModelTest(TestCase):

    def setUp(self):
        self.autism_image = Autism_Image.objects.create(
            image_id=1,
            child_id=1,
            image_upload='http://example.com/image.jpg',
            updated_at=timezone.now(),
            created_at=timezone.now()
        )
    def test_create_autism_results(self):
        """Test creating an Autism_Results instance."""
        results = Autism_Results.objects.create(
            results_id=1,
            image_id=self.autism_image,
            result='Positive',
            updated_at=timezone.now(),
            created_at=timezone.now()
        )
        
        self.assertEqual(results.results_id, 1)
        self.assertEqual(results.image_id, self.autism_image)
        self.assertEqual(results.result, 'Positive')
        self.assertIsNotNone(results.updated_at)
        self.assertIsNotNone(results.created_at)
        
    def test_string_representation(self):
        """Test the string representation of Autism_Results."""
        autism_result = Autism_Results.objects.create(
            results_id=2,
            image_id=self.autism_image,
            result='Negative',
            updated_at=timezone.now(),
            created_at=timezone.now()
        )
        
        self.assertEqual(str(autism_result), 'Negative')

    def test_field_constraints(self):
        """Test field constraints for Autism_Results."""
        autism_results_data = {
            'results_id': 1,
            'image_id': self.autism_image,
            'result': 'Positive',
            'updated_at': timezone.now(),
            'created_at': timezone.now()
        }
        Autism_Results.objects.create(**autism_results_data)

        with self.assertRaises(IntegrityError):
            Autism_Results.objects.create(
                image_id=self.autism_image,
                result='No Result',
                updated_at=timezone.now(),
                created_at=timezone.now()
            )

    def test_default_foreign_key(self):
        """Test that the default value for image_id is set correctly."""
        default_result = Autism_Results.objects.create(
            results_id=3,
            result='Default Image Test',
            updated_at=timezone.now(),
            created_at=timezone.now()
        )

        self.assertIsNotNone(default_result.image_id)