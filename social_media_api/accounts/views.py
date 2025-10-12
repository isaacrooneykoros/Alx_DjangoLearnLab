from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import CustomUser  # <-- use CustomUser instead of User
from django.shortcuts import get_object_or_404


class RegisterView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()  # <-- required line
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        data = UserSerializer(user).data
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': UserSerializer(user).data})


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
def follow_view(request, user_id):
    target = get_object_or_404(CustomUser, pk=user_id)
    user = request.user
    if user == target:
        return Response({'detail': 'Cannot follow yourself'}, status=400)
    user.following.add(target)
    return Response({'detail': 'followed'}, status=200)


@api_view(['POST'])
def unfollow_view(request, user_id):
    target = get_object_or_404(CustomUser, pk=user_id)
    user = request.user
    user.following.remove(target)
    return Response({'detail': 'unfollowed'}, status=200)
