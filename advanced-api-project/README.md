# 📚 Advanced API Project – Django REST Framework

This project is part of **Alx_DjangoLearnLab**, focused on building advanced APIs using Django REST Framework (DRF).  
It demonstrates **custom serializers, generic views, filtering/searching/ordering, and unit testing** in a clean, modular Django setup.

---

## 🚀 Project Setup

### 1. Clone & Setup Environment
```bash
git clone https://github.com/isaacrooneykoros/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/advanced-api-project

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


2. Install Dependencies
pip install django djangorestframework django-filter


3. Start Django Project & App
django-admin startproject advanced_api_project .
python manage.py startapp api



4. Configure Installed Apps
Edit advanced_api_project/settings.py:
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'django_filters',
    'api',
]



5. Database Setup
Run migrations:
python manage.py makemigrations
python manage.py migrate


6. Create Superuser
python manage.py createsuperuser
🏗️ Models
We define two models in api/models.py:

Author
name: CharField – stores the author’s name.

Book
title: CharField – stores the book’s title.

publication_year: IntegerField – year of publication.

author: ForeignKey – links to an Author (one-to-many).

📌 Relationship:

One Author can have many Books.

The related_name='books' on the ForeignKey allows us to access all an author’s books via author.books.all().

🛠️ Serializers
Defined in api/serializers.py:

BookSerializer
Serializes all fields in the Book model.
Includes custom validation to ensure the publication_year is not in the future.
def validate_publication_year(self, value):
    current_year = date.today().year
    if value > current_year:
        raise serializers.ValidationError("Publication year cannot be in the future.")
    return value
AuthorSerializer
Serializes the name field.

Includes a nested BookSerializer to list related books.
Example Response:
{
  "name": "George Orwell",
  "books": [
    {
      "title": "1984",
      "publication_year": 1949,
      "author": 1
    }
  ]
}



🌐 API Views
Views are defined in api/views.py using generic views.

Endpoints
Endpoint	Method	Description	Permissions
/api/books/	GET	List all books	Public
/api/books/	POST	Create a new book	Authenticated users
/api/books/<id>/	GET	Retrieve a single book	Public
/api/books/<id>/	PUT	Update a book	Authenticated users
/api/books/<id>/	DELETE	Delete a book	Authenticated users

Permissions
Read (GET) → allowed for everyone.

Write (POST, PUT, DELETE) → restricted to authenticated users.

This is achieved by overriding get_permissions() in the views.

🔎 Filtering, Searching & Ordering
Enabled in BookListCreateView with DRF’s filtering system.




Settings (advanced_api_project/settings.py)
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ]
}


View (api/views.py)
filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
filterset_fields = ['title', 'author__name', 'publication_year']
search_fields = ['title', 'author__name']
ordering_fields = ['title', 'publication_year']


Example Queries

Filtering:
/api/books/?title=1984
/api/books/?author__name=Rowling
/api/books/?publication_year=1997

Searching:
/api/books/?search=Orwell

Ordering:
/api/books/?ordering=publication_year
/api/books/?ordering=-title

🧪 Unit Testing
Tests are located in api/tests/test_views.py.

Covered Scenarios
Listing all books.

Creating, updating, and deleting a Book.

Permission enforcement (unauthenticated users cannot create/update/delete).

Filtering, searching, and ordering.


Run Tests
python manage.py test api
If all tests pass, your API is working as expected.


🧾 Example API Usage

1. Create an Author (via shell or admin)
from api.models import Author
a = Author.objects.create(name="J.K. Rowling")


2. Create a Book
POST /api/books/
Content-Type: application/json
Authorization: Token <your-token>

{
  "title": "Harry Potter and the Philosopher's Stone",
  "publication_year": 1997,
  "author": 1
}

3. Get All Books
GET /api/books/


4. Filter Books by Author
GET /api/books/?author__name=Rowling


5. Search Books
GET /api/books/?search=Harry



📂 Project Structure
advanced-api-project/
│── advanced_api_project/   # Django project settings
│   └── settings.py
│── api/                    # Main app
│   ├── models.py           # Author & Book models
│   ├── serializers.py      # Custom DRF serializers
│   ├── views.py            # Generic API views
│   ├── urls.py             # API routes
│   └── tests/              # Unit tests
│── manage.py
│── README.md
✅ Summary
This project demonstrates:

Custom serializers with validation & nested relationships.

Generic views for CRUD operations.

Permissions for secure API access.

Filtering, searching, ordering for usability.

Unit tests ensuring API integrity.