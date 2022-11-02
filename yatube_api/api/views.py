from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnly
from posts.models import Comment, Follow, Group, Post
from .serializers import (CommentSerializer,
                          FollowSerializer,
                          GroupsSerializer,
                          PostSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_queryset(self):
        return Follow.objects.get(user=self.kwargs.get('user'))
