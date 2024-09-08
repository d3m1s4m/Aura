from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

user_post_detail = views.UserPostViewSet.as_view(
    {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
)
user_post_list = views.UserPostViewSet.as_view(
    {'get': 'list', 'post': 'create'}
)

post_comment_detail = views.PostCommentViewSet.as_view(
    {'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'post': 'create'}
)
post_comment_list = views.PostCommentViewSet.as_view(
    {'get': 'list', 'post': 'create'}
)

post_like_detail = views.PostLikeViewSet.as_view(
    {'get': 'retrieve', 'delete': 'destroy'}
)
post_like_list = views.PostLikeViewSet.as_view(
    {'get': 'list', 'post': 'create'}
)

router = DefaultRouter()
router.register('tags', views.TagViewSet, basename='tag')
router.register('feed', views.FeedViewSet, basename='feed')
router.register('posts', views.UserPostViewSet, 'user-posts')

tags_router = routers.NestedDefaultRouter(router, 'tags', lookup='tag')
tags_router.register('posts', views.TagPostsViewSet, basename='tag-posts')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(tags_router.urls)),
    path('<str:username>/posts/', user_post_list, name='user-post-list'),
    path('<str:username>/posts/<int:pk>/', user_post_detail, name='user-post-detail'),
    path('<str:username>/posts/<int:post_id>/comments/', post_comment_list, name='post-comment-list'),
    path('<str:username>/posts/<int:post_id>/comments/<int:pk>/', post_comment_detail, name='post-comment-detail'),
    path('<str:username>/posts/<int:post_id>/likes/', post_like_list, name='post-like-list'),
    path('<str:username>/posts/<int:post_id>/likes/<int:pk>/', post_like_detail, name='post-like-detail'),
]
