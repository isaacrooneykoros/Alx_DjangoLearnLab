from django.urls import path
from .views import RegisterView, login_view, ProfileView, follow_view, unfollow_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', follow_view, name='follow'),
    path('unfollow/<int:user_id>/', unfollow_view, name='unfollow'),
]
