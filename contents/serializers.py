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
        fields = ('id', 'user', 'caption', 'media', 'location')


class PostNotificationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    media = MediaSerializer(many=True)

    class Meta:
        model = Post
        fields = ('caption', 'media', 'location', 'created_at')


class CreatePostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, required=True)

    class Meta:
        model = Post
        fields = ('caption', 'location', 'media')

    @staticmethod
    def validate_caption(value):
        """ensure the caption does not exceed a specified length."""
        max_length = 400
        if len(value) > max_length:
            raise serializers.ValidationError(f'Caption cannot exceed {max_length} characters.')
        return value

    @staticmethod
    def validate_media(value):
        """ensure that media is attached to the post."""
        if len(value) == 0:
            raise serializers.ValidationError('You must attach at least one media file.')
        return value

    def create(self, validated_data):
        # extract media data from the validated data
        media_data = self.context['request'].FILES.getlist('media')  # get media files from the request
        post = Post.objects.create(**validated_data)  # create the post first

        # handle media creation for the post
        for media_file in media_data:
            Media.objects.create(post=post, file=media_file)

        return post
