from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

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
    
class PostCRUDAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('author', 'a@a.com', 'password123')
        self.other = User.objects.create_user('other', 'o@o.com', 'password123')
        self.post = Post.objects.create(title='T1', content='C1', author=self.user)

    def test_list_and_detail_public(self):
        resp = self.client.get(reverse('post-list'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('post-detail', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('post-create'))
        self.assertNotEqual(resp.status_code, 200)  # redirect to login
        self.client.login(username='author', password='password123')
        resp = self.client.get(reverse('post-create'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(reverse('post-create'), {'title': 'New', 'content': 'Body'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New').exists())

    def test_update_only_author(self):
        self.client.login(username='other', password='password123')
        resp = self.client.get(reverse('post-update', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 403)  # UserPassesTestMixin returns 403 for failed test
        self.client.login(username='author', password='password123')
        resp = self.client.get(reverse('post-update', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_delete_only_author(self):
        self.client.login(username='other', password='password123')
        resp = self.client.post(reverse('post-delete', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 403)
        self.client.login(username='author', password='password123')
        resp = self.client.post(reverse('post-delete', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

