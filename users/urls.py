from django.urls import path, include

from users import views


urlpatterns = [
    path('', views.UsersListAPIView.as_view(), name='user-list'),
]
