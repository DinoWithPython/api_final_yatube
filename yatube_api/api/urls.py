from django.urls import include, path
from rest_framework import routers

from api.views import CommentViewSet, FollowViewSet, GroupsViewSet, PostViewSet

API_VERSION = 'v1'

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupsViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment')
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path(f'{API_VERSION}/', include(router.urls)),
    path(f'{API_VERSION}/', include('djoser.urls.jwt')),
]
