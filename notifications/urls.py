from django.urls import path

from notifications import views


urlpatterns = [
    path('', views.NotificationListAPIView.as_view(), name='notification-list'),
]
