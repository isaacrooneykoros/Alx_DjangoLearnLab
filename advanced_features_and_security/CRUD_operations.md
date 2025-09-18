# CRUD Operations on the Book Model

This document records the commands executed in the Django shell to perform Create, Retrieve, Update, and Delete (CRUD) operations on the `Book` model, along with their actual outputs.


## 1. CREATE

```python
from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book  # check representation

#Output
<Book: 1984 by George Orwell (1949)>


# Retrieve the created book
b = Book.objects.get(id=book.id)
b.title, b.author, b.publication_year

#Output
('1984', 'George Orwell', 1949)


# Update the title of the book
b.title = "Nineteen Eighty-Four"
b.save()
Book.objects.get(id=b.id).title

#Output
'Nineteen Eighty-Four'


# Delete the book instance
b.delete()

# Confirm deletion
list(Book.objects.all())

#Output
(1, {'bookshelf.Book': 1})
[]
