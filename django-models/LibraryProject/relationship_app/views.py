from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    permission_required,
)
from django import forms
from .models import Book, Library


# ----------------------------
# Forms
# ----------------------------
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]


# ----------------------------
# Home
# ----------------------------
def home(request):
    return HttpResponse(
        "<h1>Welcome to the Library App</h1>"
        "<p>Go to <a href='/books/'>Books</a></p>"
    )


# ----------------------------
# Books
# ----------------------------
def list_books(request):
    books = Book.objects.all()
    return render(request, "list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "library_detail.html"
    context_object_name = "library"


# ----------------------------
# Authentication
# ----------------------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after registration
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "relationship_app/login.html"


class CustomLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"


# ----------------------------
# Role Helpers
# ----------------------------
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"


def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"


def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"


# ----------------------------
# Role-based Views
# ----------------------------
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


# ----------------------------
# Book CRUD (with permissions)
# ----------------------------
@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm()
    return render(request, "relationship_app/add_book.html", {"form": form})


@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm(instance=book)
    return render(request, "relationship_app/edit_book.html", {"form": form, "book": book})


@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "relationship_app/delete_book.html", {"book": book})
