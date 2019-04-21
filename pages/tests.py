from django.http import HttpRequest
from django.test import TestCase

from . import views

# Create your tests here.

class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_check_incorrect(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'This should not happen')