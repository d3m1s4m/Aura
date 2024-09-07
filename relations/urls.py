from django.urls import path

from relations import views


urlpatterns = [
    path('followers/<str:username>/', views.FollowerListAPIView.as_view(), name='follower-list'),
    path('followings/<str:username>/', views.FollowingListAPIView.as_view(), name='following-list'),
    path('sent-requests/', views.SentRequestListAPIView.as_view(), name='sent-requests'),
    path('received-requests/', views.ReceivedRequestListAPIView.as_view(), name='received-requests'),
    path('blocked-users/', views.BlockedUsersListAPIView.as_view(), name='blocked-users'),
]
