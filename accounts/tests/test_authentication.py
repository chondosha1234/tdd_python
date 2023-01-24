from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import HttpRequest

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()

class AuthenticateTest(TestCase):

    def test_returns_None_if_no_token(self):
        request = HttpRequest()
        result = PasswordlessAuthenticationBackend().authenticate(request, 'no-such-token')
        self.assertIsNone(result)

    def test_returns_existing_user_with_correct_email(self):
        request = HttpRequest()
        email = 'george@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(request, token.uid)
        existing_user = User.objects.get(email=email)
        self.assertEqual(user, existing_user)

    def test_returns_new_user_with_correct_email(self):
        request = HttpRequest()
        email = 'george@example.com'
        new_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(request, token.uid)
        self.assertEqual(user, new_user)

class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        User.objects.create(email='jason@example.com')
        desired_user = User.objects.create(email='george@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user('george@example.com')
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('george@example.com')
        )
