from django.db import models

class Author(models.Model):
    # Stores author information
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    # Stores book details and links to an Author
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
