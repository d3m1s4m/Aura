from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import CursorPagination

from contents.models import Tag, Post, PostTag
from contents.serializers import TagSerializer, PostSerializer
from custom_lib.common_permissions import IsAdminOrReadOnly
from relations.models import BlockRelation, FollowRelation


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    ordering = ('-created_at',)
    ordering_fields = ('created_at', 'name')
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    search_fields = ('name__istartswith',)


class TagPostsViewSet(ModelViewSet):
    serializer_class = PostSerializer

    ordering = ('-created_at',)
    ordering_fields = ('created_at',)
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated,)
    search_fields = ('user__username__istartswith',)

    def get_queryset(self):
        tag_id = self.kwargs['tag_pk']
        user = self.request.user

        # filter posts that are tagged with the specific tag
        queryset = Post.objects.filter(tags__tag_id=tag_id)

        return queryset
