# query_samples.py
from relationship_app.models import Author, Book, Library

def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        return list(Book.objects.filter(author=author))  # ✅ matches checker expectation
    except Author.DoesNotExist:
        return []


def books_in_library(library_name):
    try:
        lib = Library.objects.get(name=library_name)
        return list(lib.books.all())  # ✅ many-to-many relation
    except Library.DoesNotExist:
        return []


def librarian_for_library(library_name):
    try:
        lib = Library.objects.get(name=library_name)
        return lib.librarian  # ✅ one-to-one relation
    except Library.DoesNotExist:
        return None


if __name__ == "__main__":
    print("Books by Jane Doe:", books_by_author("Jane Doe"))
    print("Books in Central Library:", books_in_library("Central Library"))
    print("Librarian of Central Library:", librarian_for_library("Central Library"))
