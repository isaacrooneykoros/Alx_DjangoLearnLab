
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('bookshelf.urls', namespace='bookshelf')),
    path('accounts/', include('django.contrib.auth.urls')),

]
