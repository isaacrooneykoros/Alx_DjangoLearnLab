
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("accounts.urls")),  # Includes URL patterns from the accounts app for authentication and user management.
    path('books/', include('bookshelf.urls', namespace='bookshelf')),
    path('accounts/', include('django.contrib.auth.urls')),

]
