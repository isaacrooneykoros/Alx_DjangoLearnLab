# UPDATE Operation

```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(id=1)

# Update the title of the book
book.title = "Nineteen Eighty-Four"
book.save()

# Verify update
Book.objects.get(id=book.id).title

# Output
'Nineteen Eighty-Four'
