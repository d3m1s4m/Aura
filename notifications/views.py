from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationListAPIView(ListAPIView):
    serializer_class = NotificationSerializer

    filterset_fields = ('notification_type', 'is_read')
    ordering = ('-created_at',)
    ordering_fields = ('created_at',)
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated,)
    search_fields = ('sender__username__istartswith', 'post')

    def get_queryset(self):
        user = self.request.user

        return Notification.objects.filter(receiver=user)
