from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response

from custom_lib.common_permissions import ReadOnly, CanViewUserPermission
from relations.models import FollowRelation, BlockRelation
from relations.serializers import FollowerSerializer, FollowingSerializer, BlockedSerializer, FollowSerializer

User = get_user_model()


class FollowerListAPIView(ListAPIView):
    serializer_class = FollowerSerializer

    ordering = ('-created_at',)
    ordering_fields = ('created_at',)
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated, ReadOnly, CanViewUserPermission)
    search_fields = ('from_user__username__istartswith',)

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = self.request.user

        queryset = FollowRelation.objects.filter(to_user__username=username, is_accepted=True)

        # exclude users from blocked users and accounts that have blocked the user
        blocked_users = BlockRelation.objects.filter(blocker=user).values_list('blocked', flat=True)
        blocker_users = BlockRelation.objects.filter(blocked=user).values_list('blocker', flat=True)
        queryset = queryset.exclude(from_user_id__in=blocked_users).exclude(from_user_id__in=blocker_users)

        return queryset


class FollowingListAPIView(ListAPIView):
    serializer_class = FollowingSerializer

    ordering = ('-created_at',)
    ordering_fields = ('created_at',)
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated, ReadOnly, CanViewUserPermission)
    search_fields = ('to_user__username__istartswith',)

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = self.request.user

        queryset = FollowRelation.objects.filter(from_user__username=username, is_accepted=True)

        # exclude users from blocked users and accounts that have blocked the user
        blocked_users = BlockRelation.objects.filter(blocker=user).values_list('blocked', flat=True)
        blocker_users = BlockRelation.objects.filter(blocked=user).values_list('blocker', flat=True)
        queryset = queryset.exclude(to_user_id__in=blocked_users).exclude(to_user_id__in=blocker_users)

        return queryset


class SentRequestListAPIView(ListAPIView):
    serializer_class = FollowingSerializer

    ordering = ('-created_at',)
    ordering_fields = ('created_at',)
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated, ReadOnly)
    search_fields = ('to_user__username__istartswith',)

    def get_queryset(self):
        user = self.request.user

        return FollowRelation.objects.filter(from_user=user, is_accepted=False)


class ReceivedRequestListAPIView(ListAPIView):
    serializer_class = FollowerSerializer

    ordering = ('-created_at',)
    ordering_fields = ('created_at',)
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated, ReadOnly)
    search_fields = ('from_user__username__istartswith',)

    def get_queryset(self):
        user = self.request.user

        return FollowRelation.objects.filter(to_user=user, is_accepted=False)


class BlockedUsersListAPIView(ListAPIView):
    serializer_class = BlockedSerializer

    ordering = ('-created_at',)
    ordering_fields = ('created_at',)
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated, ReadOnly)
    search_fields = ('blocked__username__istartswith',)

    def get_queryset(self):
        user = self.request.user

        return BlockRelation.objects.filter(blocker=user)


class FollowCreateDestroyAPIView(CreateAPIView, DestroyAPIView):
    queryset = FollowRelation.objects.none()
    serializer_class = FollowSerializer
    lookup_field = 'username'

    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        # include the request in the context along with the username
        context = super().get_serializer_context()
        context['username'] = self.kwargs['username']
        return context

    def get_object(self):
        from_user = self.request.user
        username = self.kwargs['username']
        to_user = get_object_or_404(User, username=username)

        # retrieve the FollowRelation object to be deleted
        follow_relation = get_object_or_404(FollowRelation, from_user=from_user, to_user=to_user)
        return follow_relation

    def delete(self, request, *args, **kwargs):
        # use get_object to retrieve the instance to be deleted
        self.object = self.get_object()
        self.object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





