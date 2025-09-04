# CREATE Operation

```python
from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book  # check representation

#Output
<Book: 1984 by George Orwell (1949)>
