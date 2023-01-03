from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.test.client import Client
from django.template.loader import render_to_string
import re

from lists.views import home_page
from lists.models import Item


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


class ItemModelTest(TestCase):

    def test_save_and_retrieve_item(self):
        first_item = Item()
        first_item.text = "The first item"
        first_item.save()

        second_item = Item()
        second_item.text = "The second item"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved = saved_items[0]
        second_saved = saved_items[1]
        self.assertEqual(first_saved.text, "The first item")
        self.assertEqual(second_saved.text, "The second item")
