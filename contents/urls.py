from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

user_post_detail = views.UserPostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
user_post_list = views.UserPostViewSet.as_view({'get': 'list', 'post': 'create'})

router = DefaultRouter()
router.register('tags', views.TagViewSet, basename='tag')
router.register('feed', views.FeedViewSet, basename='feed')
router.register('post', views.UserPostViewSet, 'user-post')

tags_router = routers.NestedDefaultRouter(router, 'tags', lookup='tag')
tags_router.register('posts', views.TagPostsViewSet, basename='tag-posts')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(tags_router.urls)),
    path('<str:username>/posts/', user_post_list, name='user-post-list'),
    path('<str:username>/posts/<int:pk>/', user_post_detail, name='user-post-detail'),
]
