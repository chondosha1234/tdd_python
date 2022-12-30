from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.test.client import Client
from django.template.loader import render_to_string
import re

from lists.views import home_page


# Create your tests here.
class HomePageTest(TestCase):

    def setUp(self):
        self.client = Client()

    """
    This function strips the auto generated csrf token from rendered html pages
    in order to compare the html page strings. This was needed in order to follow along
    with the text book examples. 
    """
    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def test_root_url_resolve_to_home_page(self):
        found = resolve('/lists/')
        self.assertEquals(found.func, home_page)

    def test_home_page_returns(self):
        response = self.client.get('/lists/')
        self.assertEquals(response.templates[0].name, 'home.html')
        self.assertTemplateUsed(response, 'home.html')
        #request = HttpRequest()
        #response = home_page(request)
        #self.assertEqual(template, 'home.html')

    def test_home_page_save_post(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)
        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})
        self.assertEqual(self.remove_csrf(response.content.decode()), self.remove_csrf(expected_html))
