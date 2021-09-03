from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Create an account
class AccountPageTest(TestCase):
    def test_account_creation(self):
        response = self.client.post(reverse('register'),
                                    data={"username": "Bob",
                                          "email": "bob@mail.com",
                                          "password1": "monpassword23",
                                          "password2": "monpassword23"})
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username="Bob")
        self.assertEqual(new_user.username, "Bob")
        # self.assertEqual(response.status_code, 302)

    def test_logged_out(self):
        response = self.client.get(reverse('logged_out'))
        self.assertEqual(response.status_code, 200)

    def test_registration_ok(self):
        response = self.client.get(reverse('registration_ok'))
        self.assertEqual(response.status_code, 200)
