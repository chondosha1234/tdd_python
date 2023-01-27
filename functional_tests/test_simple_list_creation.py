from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
import time

class NewVisitorTest(FunctionalTest):

    def test_start_and_save_list(self):
        #User goes to home page
        self.browser.get(self.live_server_url + reverse('home'))

        #page title mentions 'To Do' list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        #user invited to enter to-do item
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        #user types "buy bread" into text box
        inputbox.send_keys('Buy Bread')
        #when user presses enter the page updates and has list
        #"1: Buy Bread" as item on list
        inputbox.send_keys(Keys.ENTER)
        #page creates url after first item entered
        time.sleep(2)
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')

        #user enters "buy milk"
        #self.browser.refresh()
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy Milk')
        inputbox.send_keys(Keys.ENTER)

        #page updates again and now has 2 entries
        #self.browser.refresh() # added to deal with stale elements
        self.wait_for_row_in_table("1: Buy Bread")
        self.wait_for_row_in_table("2: Buy Milk")

        #New user2 visits site
        #use new browser session to make sure no cookies from user1
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #user2 visists home page
        # user1 list is not there
        self.browser.get(self.live_server_url + reverse('home'))
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy Bread', page_text)
        self.assertNotIn('Buy Milk', page_text)

        # user2 starts new list by entering item
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy Borshch')
        inputbox.send_keys(Keys.ENTER)

        #user2 gets their own url
        time.sleep(2)
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user_list_url, user2_list_url)

        #again check to make sure user1 list not on page
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy Bread', page_text)
        self.assertIn('Buy Borshch', page_text)

        #page should retain list information
        #page generates unique url for user with explanatory text

        # user visits the url and checks the list

        self.browser.quit()
