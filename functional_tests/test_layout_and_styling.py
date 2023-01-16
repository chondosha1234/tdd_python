from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from django.urls import reverse

MAX_WAIT = 10

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        #user goes to home page
        self.browser.get(self.live_server_url + reverse('home'))
        self.browser.set_window_size(1024, 728)

        #the input box is centered
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )
