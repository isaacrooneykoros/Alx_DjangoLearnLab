# bookshelf/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm
from .forms import ExampleForm  

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/form_example.html', {'form': form})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/confirm_delete.html', {'book': book})

def example_form_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()  # saves Book instance securely
            return redirect("bookshelf:book_list")
    else:
        form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})
