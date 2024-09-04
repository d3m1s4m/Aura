from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('email', 'username', 'password')


class UserSerializer(BaseUserSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = (
            'id', 'email', 'username', 'avatar', 'first_name', 'last_name',
            'bio', 'is_verified', 'is_private', 'followers_count', 'followings_count'
        )

    @staticmethod
    def get_followers_count(user):
        return user.followers.count()

    @staticmethod
    def get_followings_count(user):
        return user.followings.count()
