from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_start_and_save_list(self):
        #User goes to home page
        self.browser.get('http://localhost:8000/lists/')

        #page title mentions 'To Do' list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        #user invited to enter to-do item
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        #user types "buy bread" into text box
        inputbox.send_keys('Buy Bread')
        #when user presses enter the page updates and has list
        #"1: Buy Bread" as item on list
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertTrue(any(row.text == '1: Buy Bread' for row in rows))

        #There is still text box entry for more items
        self.fail('Finish Test')
        #user enters "buy milk"
        #page updates again and now has 2 entries

        #page should retain list information
        #page generates unique url for user with explanatory text

        # user visits the url and checks the list

        browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
