from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from activities.models import Comment
from users.serializers import UserLightSerializer


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text',)

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

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text')


class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()
    replies = CommentReplySerializer(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'replies')
