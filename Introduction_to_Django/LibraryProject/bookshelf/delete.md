# DELETE Operation

```python
from bookshelf.models import Book

# Delete the book instance
b = Book.objects.get(id=book.id)
b.delete()

# Confirm deletion
list(Book.objects.all())

#Output
(1, {'bookshelf.Book': 1})
[]
