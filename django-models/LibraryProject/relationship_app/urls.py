from django.urls import path
from .views import (
    home, LibraryDetailView,
    register, CustomLoginView, CustomLogoutView,
    admin_view, librarian_view, member_view,
    add_book, edit_book, delete_book
)
from .views import list_books

urlpatterns = [
    # Home
    path('', home, name='home'),

    # Books
    path('books/', list_books, name='list_books'),
    path('books/add/', add_book, name='add_book'),
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),

    # Library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Auth
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Role-based access
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
]
