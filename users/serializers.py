from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

User = get_user_model()


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


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'avatar', 'is_verified')
