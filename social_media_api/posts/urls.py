from django.urls import path, include
from .views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter
from .views import FeedView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    # feed endpoint:
    path('feed/', PostViewSet.as_view({'get':'list'}), name='feed'),  # we'll filter feed by query param in view or create a separate view below
    path('feed/', FeedView.as_view(), name='feed'),
]
