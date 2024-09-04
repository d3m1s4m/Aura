from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import CursorPagination

from contents.models import Tag
from contents.serializers import TagSerializer
from custom_lib.permissions import IsAdminOrReadOnly


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    pagination_class = CursorPagination
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name__istartswith',)
