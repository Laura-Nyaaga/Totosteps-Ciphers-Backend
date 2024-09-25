from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from child.models import Child
from autism_image.models import Autism_Image
import tempfile

User = get_user_model()

class AutismImageTests(TestCase):

    def setUp(self):
        self.parent_user = User.objects.create_user(
            email='parent@example.com',
            password='testpassword123',
            role=User.PARENT,
            first_name='Test',
            last_name='Parent'
        )

        self.child = Child.objects.create(
            username='child_user',
            date_of_birth='2020-01-01',
            parent=self.parent_user
        )

        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=tempfile.NamedTemporaryFile(suffix=".jpg").read(),
            content_type='image/jpeg'
        )

    def test_upload_image_success(self):
        autism_image = Autism_Image.objects.create(
            child=self.child,
            image_upload=self.test_image
        )
        self.assertEqual(autism_image.child, self.child)
        self.assertTrue(autism_image.image_upload)

    def test_upload_image_without_child(self):
        autism_image = Autism_Image(
            image_upload=self.test_image
        )
        with self.assertRaises(ValidationError):
            autism_image.full_clean()

    def test_upload_image_without_image(self):
        autism_image = Autism_Image(
            child=self.child
        )
        with self.assertRaises(ValidationError):
            autism_image.full_clean()

    def test_upload_invalid_image_format(self):
        invalid_file = SimpleUploadedFile(
            name='test_file.txt',
            content=b'This is not an image.',
            content_type='text/plain'
        )
        autism_image = Autism_Image(
            child=self.child,
            image_upload=invalid_file
        )
        with self.assertRaises(ValidationError):
            autism_image.full_clean()

    def tearDown(self):
        self.test_image.close()
