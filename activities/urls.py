from django.urls import path, include
from rest_framework.routers import DefaultRouter

from activities import views

like_list = views.LikeViewSet.as_view(
    {'get': 'list', 'post': 'create'}
)
like_detail = views.LikeViewSet.as_view(
    {'delete': 'destroy'}
)

router = DefaultRouter()
router.register('comments', views.CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
    path('likes/', like_list, name='like-list'),
    path('likes/<int:pk>', like_detail, name='like-detail'),
]
