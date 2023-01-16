from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.test.client import Client
from django.template.loader import render_to_string
import re

from lists.views import home_page
from lists.models import Item, List


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
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_home_page_returns(self):
        response = self.client.get('/')
        self.assertEquals(response.templates[0].name, 'home.html')
        self.assertTemplateUsed(response, 'home.html')
        #request = HttpRequest()
        #response = home_page(request)
        #self.assertEqual(template, 'home.html')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list 1', list=other_list)
        Item.objects.create(text='other list 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id))

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'other list 1')
        self.assertNotContains(response, 'other list 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/%d/' % (correct_list.id))

        self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):

    def test_save_post_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(response.status_code, 302)
        new_list = List.objects.first()
        self.assertEqual(response['location'], '/lists/%d/' % (new_list.id))
        self.assertRedirects(response, '/lists/%d/' % (new_list.id))

class NewItemTest(TestCase):

    def test_can_save_post_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id),
            data={'item_text': 'A new item for existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id),
            data={'item_text': 'A new item for existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id))
