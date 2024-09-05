from django.utils.timesince import timesince
from rest_framework import serializers

from contents.serializers import PostNotificationSerializer
from notifications.models import Notification
from users.serializers import UserLightSerializer


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserLightSerializer()
    post = PostNotificationSerializer()
    notification_type = serializers.CharField(source='get_notification_type_display', read_only=True)
    time_since = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('notification_type', 'sender', 'post', 'is_read', 'time_since', 'created_at')

    @staticmethod
    def get_time_since(obj):
        return timesince(obj.created_at)
