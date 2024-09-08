from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from relations.models import FollowRelation, BlockRelation
from users.serializers import UserLightSerializer

User = get_user_model()


class FollowerSerializer(serializers.ModelSerializer):
    from_user = UserLightSerializer()
    follow_back = serializers.SerializerMethodField()

    class Meta:
        model = FollowRelation
        fields = ('from_user', 'follow_back', 'created_at')

    @staticmethod
    def get_follow_back(obj):
        return FollowRelation.objects.filter(from_user=obj.to_user, to_user=obj.from_user).exists()


class FollowingSerializer(serializers.ModelSerializer):
    to_user = UserLightSerializer()
    follow_back = serializers.SerializerMethodField()

    class Meta:
        model = FollowRelation
        fields = ('to_user', 'follow_back', 'created_at')

    @staticmethod
    def get_follow_back(obj):
        return FollowRelation.objects.filter(from_user=obj.to_user, to_user=obj.from_user).exists()


class BlockedSerializer(serializers.ModelSerializer):
    blocked = UserLightSerializer()

    class Meta:
        model = BlockRelation
        fields = ('blocked', 'created_at')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRelation
        fields = ('id', 'from_user', 'to_user', 'is_accepted')
        read_only_fields = ('id', 'from_user', 'to_user', 'is_accepted')

    def validate(self, attrs):
        from_user = self.context['request'].user
        username = self.context['username']

        # retrieve 'to_user' by username
        try:
            to_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError(_("The user with this username does not exist."))

        # check if user is trying to follow themselves
        if from_user == to_user:
            raise ValidationError(_("You cannot follow yourself."))

        # check if the follow relationship already exists
        if FollowRelation.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise ValidationError(_("You are already following this user."))

        # check if the user has been blocked
        if BlockRelation.objects.filter(blocker=to_user, blocked=from_user).exists():
            raise ValidationError(_("You cannot follow this user."))

        # check if the from_user has blocked the to_user
        if BlockRelation.objects.filter(blocker=from_user, blocked=to_user).exists():
            raise ValidationError(_("You cannot follow this user."))

        # attach the resolved to_user to the attrs
        attrs['to_user'] = to_user

        return attrs

    def save(self, **kwargs):
        from_user = self.context['request'].user

        # set the 'from_user' to the authenticated user
        kwargs['from_user'] = from_user

        # automatically accept follow request if the profile is public
        if not self.validated_data['to_user'].is_private:
            self.validated_data['is_accepted'] = True

        return super().save(**kwargs)


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRelation
        fields = ('id', 'from_user', 'to_user', 'is_accepted')
        read_only_fields = ('id', 'from_user', 'to_user', 'is_accepted')


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockRelation
        fields = ('id', 'blocker', 'blocked')
        read_only_fields = ('id', 'blocker', 'blocked')

    def validate(self, attrs):
        blocker = self.context['request'].user
        username = self.context['username']

        try:
            blocked = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError(_("The user with this username does not exist."))

        # prevent blocking oneself
        if blocker == blocked:
            raise ValidationError(_("You cannot block yourself."))

        # prevent duplicate blocking
        if BlockRelation.objects.filter(blocker=blocker, blocked=blocked).exists():
            raise ValidationError(_("You have already blocked this user."))

        return attrs

    def save(self, **kwargs):
        blocker = self.context['request'].user
        blocked = get_object_or_404(User, username=self.context['username'])

        kwargs['blocker'] = blocker
        kwargs['blocked'] = blocked

        return super().save(**kwargs)

