from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from .models import Child
from django.utils import timezone


class ChildModelTests(TestCase):

    def test_create_child_happy_path(self):
        """Test creating a Child instance with valid data."""
        child = Child.objects.create(
            username='testuser',
            date_of_birth=date(2010, 1, 1)  
        )
        self.assertIsInstance(child, Child)
        self.assertEqual(child.username, 'testuser')
        self.assertEqual(child.date_of_birth, date(2010, 1, 1))  
        self.assertIsNotNone(child.created_at)
        self.assertIsNotNone(child.updated_at)

    def test_create_child_unhappy_path_missing_username(self):
        """Test creating a Child instance without a username raises a ValidationError."""
        child = Child(username='', date_of_birth=date(2010, 1, 1))
        with self.assertRaises(ValidationError):
            child.full_clean()  

    def test_create_child_unhappy_path_duplicate_username(self):
        """Test creating a Child instance with a duplicate username raises a ValidationError."""
        Child.objects.create(
            username='testuser',
            date_of_birth=date(2010, 1, 1)
        )
        child = Child(username='testuser', date_of_birth=date(2011, 1, 1))
        with self.assertRaises(ValidationError):
            child.full_clean()  

    def test_create_child_unhappy_path_invalid_date_of_birth(self):
        """Test creating a Child instance with a future date_of_birth raises a ValidationError."""
        future_date = timezone.now().date() + timezone.timedelta(days=1)
        child = Child(username='testuser', date_of_birth=future_date)
       


