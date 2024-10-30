from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import User

class UserModelTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='password',
            role='admin'
        )

        self.parent_user = User.objects.create_user(
            email='parent@example.com',
            password='password',
            role='parent'
        )


    def test_create_user_with_valid_data(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='password',
            role='parent'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'parent')
        self.assertFalse(user.is_superuser)

    def test_create_superuser_with_valid_data(self):
        user = User.objects.create_superuser(
            email='superuser@example.com',
            password='password'
        )
        self.assertEqual(user.email, 'superuser@example.com')
        self.assertEqual(user.role, 'admin')
        self.assertTrue(user.is_superuser)

    def test_user_can_have_admin_role_if_is_superuser(self):
        self.admin_user.clean()
        self.assertTrue(self.admin_user.is_admin)

    def test_user_can_have_parent_role(self):
        self.parent_user.clean()
        self.assertTrue(self.parent_user.is_parent)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=None,
                password='password',
                role='parent'
            )

    def test_create_user_without_role_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='test@example.com',
                password='password',
                role=None
            )

    def test_non_superuser_cannot_have_admin_role(self):
        self.parent_user.role = 'admin'
        with self.assertRaises(ValidationError):
            self.parent_user.clean()

    def test_superuser_must_have_admin_role(self):
        self.admin_user.role = 'parent'
        with self.assertRaises(ValidationError):
            self.admin_user.clean()
