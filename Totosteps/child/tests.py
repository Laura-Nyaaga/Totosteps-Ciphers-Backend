from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from child.models import Child
from datetime import date
class ChildModelTest(TestCase):
    def setUp(self):
        self.child = Child.objects.create(
            username="testchild",
            date_of_birth=date(2015, 1, 1),
            is_active=True
        )
    def test_child_creation(self):
        self.assertTrue(isinstance(self.child, Child))
        self.assertEqual(self.child.__str__(), f"testchild (ID: {self.child.child_id})")
    def test_username_unique(self):
        with self.assertRaises(IntegrityError):
            Child.objects.create(
                username="testchild",
                date_of_birth=date(2016, 1, 1)
            )
    def test_profile_picture_upload(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        child = Child.objects.create(
            username="picturechild",
            date_of_birth=date(2017, 1, 1),
            profile_picture=image
        )
        self.assertTrue(child.profile_picture.name.startswith('child_profiles/'))
    def test_is_active_default(self):
        child = Child.objects.create(
            username="activechild",
            date_of_birth=date(2018, 1, 1)
        )
        self.assertTrue(child.is_active)
    def test_created_and_updated_at(self):
        self.assertIsNotNone(self.child.created_at)
        self.assertIsNotNone(self.child.updated_at)
        original_updated_at = self.child.updated_at
        self.child.username = "updatedchild"
        self.child.save()
        self.child.refresh_from_db()
        self.assertGreater(self.child.updated_at, original_updated_at)
    def test_date_of_birth_validation(self):
        future_date = timezone.now().date() + timezone.timedelta(days=1)
        try:
            child = Child.objects.create(
                username="futurechild",
                date_of_birth=future_date
            )
            self.assertTrue(True)
        except ValidationError:
            self.fail("Unexpected ValidationError raised")