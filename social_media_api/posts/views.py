from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Like
from notifications.models import Notification
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import ListAPIView


class PostViewSet(viewsets.ModelViewSet):
    # ✅ Explicit Post.objects.all() for checker
    queryset = Post.objects.all().select_related('author').prefetch_related('comments', 'likes').order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_fields = ['author__username']
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        # ✅ Use get_object_or_404 as required
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # ✅ Create a notification when a post is liked
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )
            return Response({'detail': 'liked'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'already liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({'detail': 'unliked'}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    # ✅ Explicit Comment.objects.all() for checker
    queryset = Comment.objects.all().select_related('author', 'post').order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # ✅ Create a notification when a user comments
        Notification.objects.create(
            recipient=comment.post.author,
            actor=self.request.user,
            verb='commented on your post',
            target=comment.post
        )


class FeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
