from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from django.urls import reverse

MAX_WAIT = 10

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        #User goes to homepage and tries to submit blank list item
        #they hit enter

        #home page refreshes and has error message saying list item
        # cannot be blank

        #tries to enter item with text and it works

        # user tries to enter second duplicate item

        # list page produces similar error

        #user can add a different item after this
        self.fail('write me!')
