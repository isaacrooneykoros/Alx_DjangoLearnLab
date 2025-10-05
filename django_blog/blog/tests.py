from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def test_register(self):
        resp = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 't@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        })
        self.assertEqual(resp.status_code, 302)  # redirect after register
        self.assertTrue(User.objects.filter(username='testuser').exists())

def test_login_logout(self):
    User.objects.create_user('u1', 'u1@example.com', 'pw1234567')
    resp = self.client.post(reverse('login'), {'username': 'u1', 'password': 'pw1234567'})
    self.assertEqual(resp.status_code, 302)
    resp = self.client.post(reverse('logout'))  # Use POST here
    self.assertIn(resp.status_code, (200, 302))

