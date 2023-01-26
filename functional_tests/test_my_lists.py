from django.conf import settings
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)
        # to set a cookie you need to visit domain
        # 404 pages load quickest
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # User is a logged in user
        self.create_pre_authenticated_session('george@example.com')

        # user goes to home page and starts list
        self.browser.get(self.live_server_url)
        self.add_list_item('Some stuff')
        self.add_list_item('Other things')
        first_list_url = self.browser.current_url

        # they notice "My Lists" link
        self.browser.find_element(By.LINK_TEXT, 'My Lists').click()

        # user sees their list based on first list item
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Some stuff')
        )
        self.browser.find_element(By.LINK_TEXT, 'Some stuff').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # User decides to start another list
        self.browser.get(self.live_server_url)
        self.add_list_item('Do tasks')
        second_list_url = self.browser.current_url

        # under "My lists" the new list appears
        self.browser.find_element(By.LINK_TEXT, 'My Lists').click()
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Do tasks')
        )
        self.browser.find_element(By.LINK_TEXT, 'Do tasks').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # user logs out. "My lists" option disappears
        self.browser.find_element(By.LINK_TEXT, 'Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.LINK_TEXT('My lists'), [])
        ))
