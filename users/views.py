from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated

from relations.models import BlockRelation
from users.serializers import UserLightSerializer
from users.models import User


class UsersListAPIView(ListAPIView):
    serializer_class = UserLightSerializer

    filterset_fields = ('is_verified', 'is_private')
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated,)
    search_fields = ('username__istartswith',)

    def get_queryset(self):
        user = self.request.user

        queryset = User.objects.filter(is_active=True)

        blocker_users = BlockRelation.objects.filter(blocked=user).values_list('blocker', flat=True)

        queryset.exclude(id__in=blocker_users)

        return queryset
