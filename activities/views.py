from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from activities.models import Comment, Like
from activities.serializers import CommentListSerializer, CommentCreateSerializer, CommentDetailSerializer, \
    CommentUpdateSerializer, LikeListLightSerializer, LikeCreateSerializer, LikeListSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentListSerializer

    ordering = ('-created_at',)
    ordering_fields = ('created_at',)
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated,)
    search_fields = ('user__username__istartswith',)

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        elif self.action == 'retrieve':
            return CommentDetailSerializer
        elif self.action == 'update':
            return CommentUpdateSerializer
        return self.serializer_class


class LikeViewSet(ModelViewSet):
    serializer_class = LikeListLightSerializer

    def get_queryset(self):
        user = self.request.user
        return Like.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return LikeCreateSerializer
        return self.serializer_class
