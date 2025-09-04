# UPDATE Operation

```python
from bookshelf.models import Book

# Update the title of the book
b = Book.objects.get(id=book.id)
b.title = "Nineteen Eighty-Four"
b.save()
Book.objects.get(id=b.id).title

#Output
'Nineteen Eighty-Four'
