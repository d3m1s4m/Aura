from rest_framework import serializers

from contents.models import Tag, Post, Media
from locations.serializers import LocationSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'media_type', 'file')


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    location = LocationSerializer()
    media = MediaSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'caption', 'media')


