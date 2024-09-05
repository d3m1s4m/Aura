from rest_framework import serializers

from relations.models import FollowRelation, BlockRelation
from users.serializers import UserLightSerializer


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
