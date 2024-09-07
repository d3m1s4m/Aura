from django.urls import path, include
from rest_framework.routers import DefaultRouter

from activities import views

router = DefaultRouter()
router.register('comments', views.CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
]
