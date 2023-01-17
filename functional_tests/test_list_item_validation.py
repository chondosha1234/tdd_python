from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from django.urls import reverse

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        #User goes to homepage and tries to submit blank list item
        #they hit enter
        self.browser.get(self.live_server_url)

        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)

        #home page refreshes and has error message saying list item
        # cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
                "You can't have an empty list item"))
        #tries to enter item with text and it works
        self.browser.find_element(By.ID, 'id_new_item').send_keys('Buy milk')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy milk')

        # user tries to enter second blank item
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        # list page produces similar error

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
                "You can't have an empty list item"))

        #user can add a different item after this
        self.browser.find_element(By.ID, 'id_new_item').send_keys('Buy tea')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy milk')
        self.wait_for_row_in_table('2: Buy tea')
