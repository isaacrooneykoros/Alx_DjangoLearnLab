from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # add this
    # optionally a simple index:
    path('', TemplateView.as_view(template_name='blog/index.html'), name='home'),
]
