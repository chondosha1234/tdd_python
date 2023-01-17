from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List



class ListAndItemModelTest(TestCase):

    def test_save_and_retrieve_item(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "The second item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(list_, saved_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved = saved_items[0]
        second_saved = saved_items[1]
        self.assertEqual(first_saved.text, "The first item")
        self.assertEqual(first_saved.list, list_)
        self.assertEqual(second_saved.text, "The second item")
        self.assertEqual(second_saved.list, list_)

    def test_cannot_save_empty_list_item(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
