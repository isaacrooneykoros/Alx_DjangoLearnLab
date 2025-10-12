from django.urls import path, include
urlpatterns = [
    path('social/accounts/', include('accounts.urls')),
    path('social/notifications/', include('notifications.urls')),
    path('social/posts/', include('posts.urls')),
    
]
