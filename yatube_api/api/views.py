from rest_framework import viewsets

from posts.models import Comment, Group, Post
from .serializers import CommentSerializer, GroupsSerializer, PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get("post_id"))

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
