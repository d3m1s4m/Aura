from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from custom_lib.common_permissions import ReadOnly
from relations.models import FollowRelation, BlockRelation
from relations.serializers import FollowerSerializer, FollowingSerializer, BlockedSerializer


class FollowerListAPIView(ListAPIView):
    serializer_class = FollowerSerializer

    ordering = ('-created_at',)
    ordering_fields = ('created_at',)
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated, ReadOnly)
    search_fields = ('from_user__username__istartswith',)

    def get_queryset(self):
        user = self.request.user

        return FollowRelation.objects.filter(to_user=user, is_accepted=True)


class FollowingListAPIView(ListAPIView):
    serializer_class = FollowingSerializer

    ordering = ('-created_at',)
    ordering_fields = ('created_at',)
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated, ReadOnly)
    search_fields = ('to_user__username__istartswith',)

    def get_queryset(self):
        user = self.request.user

        return FollowRelation.objects.filter(from_user=user, is_accepted=True)


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
