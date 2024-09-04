from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

router = DefaultRouter()
router.register('tags', views.TagViewSet, basename='tag')

tags_router = routers.NestedDefaultRouter(router, 'tags', lookup='tag')
tags_router.register('posts', views.TagPostsViewSet, basename='tag-posts')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(tags_router.urls)),
]
