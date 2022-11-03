import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64')
            ext = format.split('/')[1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'
        model = Post


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Follow

    def validate(self, data):
        user = get_object_or_404(User, username=data['following'].username)
        follow = Follow.objects.filter(
            user=self.context['request'].user,
            following=user).exists()
        if user == self.context['request'].user:
            raise serializers.ValidationError(
                "Вы не можете подписаться сам на себя")
        if follow is True:
            raise serializers.ValidationError(
                "Вы уже подписаны на пользователя")
        return data
