from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()
class UserModelTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.parent_user = User.objects.create_user(
            email='parent@example.com',
            password='parentpass123',
            role='parent'
        )
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='parent'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.role, 'parent')
        self.assertFalse(user.is_superuser)
    def test_create_superuser(self):
        self.assertTrue(self.admin_user.is_superuser)
        self.assertEqual(self.admin_user.role, 'admin')
    def test_user_str_method(self):
        self.assertEqual(str(self.parent_user), 'parent@example.com')
    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='test123', role='parent')
    def test_create_user_without_role(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='test@example.com', password='test123')
    def test_create_non_superuser_with_admin_role(self):
        user = User.objects.create_user(
            email='nonsuperadmin@example.com',
            password='test123',
            role='admin'
        )
        with self.assertRaises(ValidationError):
            user.clean()
    def test_is_admin_property(self):
        self.assertTrue(self.admin_user.is_admin)
        self.assertFalse(self.parent_user.is_admin)
    def test_is_parent_property(self):
        self.assertFalse(self.admin_user.is_parent)
        self.assertTrue(self.parent_user.is_parent)