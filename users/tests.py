
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class UsersModelsTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username='bookworm',
            email='worm@example.com',
            password='securepassword123'
        )

    def test_custom_user_creation(self):

        self.assertEqual(self.user.username, 'bookworm')
        self.assertEqual(self.user.email, 'worm@example.com')
        self.assertTrue(self.user.is_active)

    def test_user_profile_creation(self):
        profile, created = UserProfile.objects.get_or_create(user=self.user)

        profile.phone = "+447123456789"
        profile.address = "221B Baker Street, London"
        profile.save()

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.phone, "+447123456789")
        self.assertEqual(str(profile), "bookworm")

        self.user.refresh_from_db()

        self.assertEqual(self.user.profile.phone, "+447123456789")

