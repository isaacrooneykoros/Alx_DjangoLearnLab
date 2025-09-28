from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Author, Book


class BookAPITests(APITestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username="tester", password="password123")

        # Create an author and a book
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="HP1", publication_year=1997, author=self.author)

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data[0])
        self.assertEqual(response.data[0]["title"], "HP1")

    def test_create_book_unauthenticated(self):
        url = reverse('book-list')
        data = {"title": "HP2", "publication_year": 1998, "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_create_book_authenticated(self):
        self.client.login(username="tester", password="password123")  # ✅ login
        url = reverse('book-list')
        data = {"title": "HP2", "publication_year": 1998, "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "HP2")

    def test_update_book_authenticated(self):
        self.client.login(username="tester", password="password123")  # ✅ login
        url = reverse('book-detail', args=[self.book.id])
        data = {"title": "HP1 Updated", "publication_year": 1997, "author": self.author.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "HP1 Updated")

    def test_delete_book_authenticated(self):
        self.client.login(username="tester", password="password123")  # ✅ login
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
