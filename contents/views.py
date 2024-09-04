from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import CursorPagination

from contents.models import Tag, Post
from contents.serializers import TagSerializer, PostSerializer
from custom_lib.common_permissions import IsAdminOrReadOnly, CanViewPostPermission
from relations.models import BlockRelation


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
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    search_fields = ('user__username__istartswith',)

    def get_queryset(self):
        """
        retrieves posts that contain a specific tag while considering the user's visibility permissions
        and relationships, including follow status and blocking.
        """
        tag_id = self.kwargs['tag_pk']
        user = self.request.user

        # filter posts that are tagged with the specific tag
        queryset = Post.objects.filter(tags__tag_id=tag_id)

        # filter posts based on visibility and follow relationship
        queryset = queryset.filter(
            Q(user=user) |
            Q(user__followers__from_user=user, user__followers__is_accepted=True) |
            Q(user__is_private=False)
        ).distinct()

        # exclude posts from blocked users and accounts that have blocked the user
        blocked_users = BlockRelation.objects.filter(blocker=user).values_list('blocked', flat=True)
        blocker_users = BlockRelation.objects.filter(blocked=user).values_list('blocker', flat=True)
        queryset = queryset.exclude(user_id__in=blocked_users).exclude(user_id__in=blocker_users)

        return queryset
