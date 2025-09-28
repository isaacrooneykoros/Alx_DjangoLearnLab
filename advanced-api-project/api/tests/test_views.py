from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Author, Book

class BookAPITests(APITestCase):

    def setUp(self):
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="HP1", publication_year=1997, author=self.author)

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        url = reverse('book-list')
        data = {"title": "HP2", "publication_year": 1998, "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # unauthenticated

    def test_update_book(self):
        url = reverse('book-detail', args=[self.book.id])
        data = {"title": "HP1 Updated", "publication_year": 1997, "author": self.author.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
