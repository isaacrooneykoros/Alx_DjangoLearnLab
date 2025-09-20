# bookshelf/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description']
        
class ExampleForm(forms.ModelForm):
    """
    Example form for demonstrating secure form handling.
    """
    class Meta:
        model = Book
        fields = ['title', 'author']  # keep it simple for the example
