from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from activities.models import Comment, Like, Save
from contents.models import Post
from contents.serializers import PostSerializer
from relations.models import FollowRelation, BlockRelation
from users.serializers import UserLightSerializer


class CommentCreateLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text',)

    @staticmethod
    def validate_text(attr):
        if len(attr) > 256:
            raise ValidationError(_("Comment text cannot be more than 256 characters."))
        return attr


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'post', 'reply_to')

    def validate(self, attrs):
        request = self.context['request']
        user = request.user

        # retrieve the post object
        post = get_object_or_404(Post, pk=attrs['post'].id)

        # check if the post is public or if the user follows the post owner or if it is the user page
        if post.user.is_private and user != post.user:
            follows = FollowRelation.objects.filter(
                from_user=user,
                to_user=post.user,
                is_accepted=True
            ).exists()

            if not follows:
                raise ValidationError(
                    _("You can't comment on this post because the user is private and you don't follow them.")
                )

        # if the account is public, check if the user is blocked
        elif not post.user.is_private and post.user != user:
            blocked = BlockRelation.objects.filter(
                blocker=post.user,
                blocked=user
            ).exists()

            if blocked:
                raise ValidationError(
                    _("You can't comment on this post.")
                )

        # check if reply_to exists and if it's valid
        if attrs.get('reply_to'):
            reply_to = attrs['reply_to']

            # ensure the reply belongs to the same post
            if reply_to.post != post:
                raise ValidationError(
                    _("You can't reply to a comment that is not part of this post.")
                )

            # prevent recursive replies
            if reply_to.reply_to is not None:
                raise ValidationError(_("Recursive replies are not allowed."))

        # only followers and post owner can send and see comments
        if (
                request.user != attrs['post'].user
                and not FollowRelation.objects.filter(from_user=request.user, to_user=attrs['post'].user).exists()):
            raise ValidationError(_("You are not allowed to perform this action"))

        # check if the user has been blocked by the post owner
        if BlockRelation.objects.filter(blocker=attrs['post'].user, blocked=request.user).exists():
            raise ValidationError(_("You have been blocked by the post owner"))

        # ensure the user is commenting on behalf of themselves
        attrs['user'] = request.user

        return attrs

    @staticmethod
    def validate_text(attr):
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
    def validate_text(attr):
        if len(attr) > 256:
            raise ValidationError(_("Comment text cannot be more than 256 characters."))
        return attr


class CommentReplySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'user')


class CommentListLightSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text')


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    reply_to = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'reply_to', 'post')

    @staticmethod
    def get_reply_to(obj):
        return {
            "id": obj.reply_to.id,
            "text": obj.reply_to.text,
            "user": obj.reply_to.user.username,
        } if obj.reply_to is not None else None


class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()
    replies = CommentReplySerializer(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'replies')


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post',)

    def validate(self, attrs):
        request = self.context['request']
        user = request.user

        # retrieve the post object
        post = get_object_or_404(Post, pk=attrs['post'].id)

        # check if the post is public or if the user follows the post owner or if it is the user page
        if post.user.is_private and user != post.user:
            follows = FollowRelation.objects.filter(
                from_user=user,
                to_user=post.user,
                is_accepted=True
            ).exists()

            if not follows:
                raise ValidationError(
                    _("You can't like this post because the user is private and you don't follow them.")
                )
        # if the account is public, check if the user is blocked
        elif post.user != user:
            blocked = BlockRelation.objects.filter(
                blocker=post.user,
                blocked=user
            ).exists()

            if blocked:
                raise ValidationError(
                    _("You can't like this post.")
                )

        # check if the user already liked the post
        if Like.objects.filter(user=user, post=post).exists():
            raise ValidationError(_("You can't like a post more than once."))

        # ensure the user is commenting on behalf of themselves
        attrs['user'] = request.user

        # Pass the validated data
        return attrs


class LikeListLightSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Like
        fields = ('id', 'post', 'created_at')


class LikeListSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()
    post = PostSerializer()

    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')


class SaveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post',)

    def validate(self, attrs):
        request = self.context['request']
        user = request.user

        # retrieve the post object
        post = get_object_or_404(Post, pk=attrs['post'].id)

        # check if the post is public or if the user follows the post owner or if it is the user page
        if post.user.is_private and user != post.user:
            follows = FollowRelation.objects.filter(
                from_user=user,
                to_user=post.user,
                is_accepted=True
            ).exists()

            if not follows:
                raise ValidationError(
                    _("You can't save this post because the user is private and you don't follow them.")
                )
        # if the account is public, check if the user is blocked
        elif post.user != user:
            blocked = BlockRelation.objects.filter(
                blocker=post.user,
                blocked=user
            ).exists()

            if blocked:
                raise ValidationError(
                    _("You can't save this post.")
                )

        # check if the user already liked the post
        if Save.objects.filter(user=user, post=post).exists():
            raise ValidationError(_("You can't save a post more than once."))

        # ensure the user is commenting on behalf of themselves
        attrs['user'] = request.user

        # Pass the validated data
        return attrs


class SaveListSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Like
        fields = ('id', 'post', 'created_at')
