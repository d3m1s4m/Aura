from django.urls import path

from relations import views


urlpatterns = [
    path('followers/<str:username>/', views.FollowerListAPIView.as_view(), name='follower-list'),
    path('followings/<str:username>/', views.FollowingListAPIView.as_view(), name='following-list'),
    path('sent-requests/', views.SentRequestListAPIView.as_view(), name='sent-requests'),
    path('received-requests/', views.ReceivedRequestListAPIView.as_view(), name='received-requests'),
    path(
        'received-requests/<str:username>/',
        views.RequestAcceptDeclineAPIView.as_view(),
        name='received-request-detail'
    ),
    path('blocked-users/', views.BlockedUsersListAPIView.as_view(), name='blocked-users'),
    path('follow/<str:username>/', views.FollowCreateDestroyAPIView.as_view(), name='follow')
]
