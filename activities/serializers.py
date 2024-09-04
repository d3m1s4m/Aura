from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from activities.models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'post', 'reply_to')

    @staticmethod
    def validate_caption(attr):
        if len(attr) > 256:
            raise ValidationError(_("Comment text cannot be more than 256 characters."))
        return attr

    @staticmethod
    def validate_reply_to(attr):
        if attr is not None and attr.reply_to is not None:
            raise ValidationError(_("Performing recursive reply is not allowed."))
        return attr


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text',)

    @staticmethod
    def validate_caption(attr):
        if len(attr) > 256:
            raise ValidationError(_("Comment text cannot be more than 256 characters."))
        return attr


class CommentReplySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'user')


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    reply_to = serializers.SerializerMethodField()
    replies = CommentReplySerializer(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'caption', 'reply_to', 'replies')

    @staticmethod
    def get_reply_to(obj):
        return {
            "id": obj.reply_to.id,
            "text": obj.reply_to.text,
            "user": obj.reply_to.user.username,
        } if obj.reply_to is not None else None
