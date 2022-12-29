from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page


# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page(self):
        found = resolve('/lists/')
        self.assertEquals(found.func, home_page)

    def test_home_page_returns(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
