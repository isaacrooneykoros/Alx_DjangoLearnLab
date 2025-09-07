# DELETE Operation

```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(id=1)

# Delete the book
book.delete()

# Verify deletion
list(Book.objects.all())

# Output
[]
