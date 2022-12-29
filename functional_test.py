from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_start_and_save_list(self):
        #User goes to home page
        self.browser.get('http://localhost:8000')

        #page title mentions 'To Do' list
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        #user invited to enter to-do item

        #user types "buy bread" into text box
        #when user presses enter the page updates and has list
        #"1: Buy Bread" as item on list

        #There is still text box entry for more items

        #user enters "buy milk"
        #page updates again and now has 2 entries

        #page should retain list information
        #page generates unique url for user with explanatory text

        # user visits the url and checks the list

        browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
