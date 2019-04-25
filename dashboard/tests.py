from django.test import TestCase
from .models import UserProfile, CustomUser

# Create your tests here.
class UserProfileTestCase(TestCase):
    '''
    Tests the UserProfile model
    '''

    def setUp(self):
        self.user = CustomUser.objects.create(username='test', email="test@test.com")
        UserProfile.objects.create(user=self.user, avatar_url='http://localhost')

    def test_avatar_url(self):
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.avatar_url, 'http://localhost')
        self.assertEqual(profile.has_profile_image(), False)
        self.assertEqual(profile.has_avatar_url(), True)
        self.assertEqual(str(profile), "test@test.com")
class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_check_incorrect(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'This should not happen')
