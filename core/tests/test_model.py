from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTests(TestCase):
    def test_create_user(self):
        """Test creation of normal user"""
        User = get_user_model()
        user = User.objects.create_user(
            username="michal", email="michal@domain.com", password="testpass123"
        )
        self.assertEqual(user.username, "michal")
        self.assertEqual(user.email, "michal@domain.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creation of super user"""
        User = get_user_model()
        user = User.objects.create_superuser(
            username="michal", email="michal@domain.com", password="testpass123"
        )
        self.assertEqual(user.username, "michal")
        self.assertEqual(user.email, "michal@domain.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
