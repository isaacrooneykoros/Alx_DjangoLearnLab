from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post , Comment

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
        
class CommentTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user('author', 'a@a.com', 'p@ssword')
        self.other = User.objects.create_user('other', 'o@o.com', 'p@ssword')
        self.post = Post.objects.create(title='Test Post', content='Body', author=self.author)

    def test_create_comment_requires_login(self):
        url = reverse('comment-create', args=[self.post.pk])
        resp = self.client.post(url, {'content': 'Nice post!'})
        # not logged in -> redirect to login
        self.assertEqual(resp.status_code, 302)
        # login then create
        self.client.login(username='other', password='p@ssword')
        resp = self.client.post(url, {'content': 'Nice post!'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.post, author=self.other).exists())

    def test_update_comment_only_author(self):
        comment = Comment.objects.create(post=self.post, author=self.other, content='Hello')
        edit_url = reverse('comment-update', args=[comment.pk])
        # another user (not comment author)
        self.client.login(username='author', password='p@ssword')
        resp = self.client.get(edit_url)
        # should be 403 (UserPassesTestMixin)
        self.assertEqual(resp.status_code, 403)
        # correct user can access
        self.client.login(username='other', password='p@ssword')
        resp = self.client.get(edit_url)
        self.assertEqual(resp.status_code, 200)

    def test_delete_comment_only_author(self):
        comment = Comment.objects.create(post=self.post, author=self.other, content='To delete')
        delete_url = reverse('comment-delete', args=[comment.pk])
        # attempt delete as not-author -> 403
        self.client.login(username='author', password='p@ssword')
        resp = self.client.post(delete_url)
        self.assertEqual(resp.status_code, 403)
        # author deletes
        self.client.login(username='other', password='p@ssword')
        resp = self.client.post(delete_url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
        
class TagSearchTests(TestCase):
    def setUp(self):
        u = User.objects.create_user('a','a@a.com','pass')
        p1 = Post.objects.create(title='Python tips', content='Some content', author=u)
        p1.tags.add('python', 'tips')
        p2 = Post.objects.create(title='Django guide', content='Django content', author=u)
        p2.tags.add('django')

    def test_tag_view(self):
        resp = self.client.get(reverse('posts-by-tag', args=['python']))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Python tips')

    def test_search_by_keyword(self):
        resp = self.client.get(reverse('search'), {'q': 'Django'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Django guide')

