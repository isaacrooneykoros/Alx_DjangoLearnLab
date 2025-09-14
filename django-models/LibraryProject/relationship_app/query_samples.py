# query_samples.py
from relationship_app.models import Author, Library, Librarian, Book


def books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        return list(Book.objects.filter(author=author))  # ✅ explicit filter
    except Author.DoesNotExist:
        return []


def books_in_library(library_name):
    """List all books in a library."""
    try:
        lib = Library.objects.get(name=library_name)
        return list(lib.books.all())  # ✅ many-to-many relation
    except Library.DoesNotExist:
        return []


def librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    try:
        return Librarian.objects.get(library__name=library_name)  # ✅ explicit query
    except Librarian.DoesNotExist:
        return None


if __name__ == "__main__":
    print("Books by Jane Doe:", books_by_author("Jane Doe"))
    print("Books in Central Library:", books_in_library("Central Library"))
    print("Librarian of Central Library:", librarian_for_library("Central Library"))
