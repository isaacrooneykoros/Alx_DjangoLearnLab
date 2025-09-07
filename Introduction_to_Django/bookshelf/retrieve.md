# RETRIEVE Operation

```python
from bookshelf.models import Book

# Retrieve the created book
b = Book.objects.get(id=book.id)
b.title, b.author, b.publication_year

#Output
('1984', 'George Orwell', 1949)
