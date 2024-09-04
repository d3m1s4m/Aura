from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from locations.models import Location
from locations.serializers import LocationSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    permission_classes = (IsAdminUser,)
    search_fields = ('name__istartswith', 'lat', 'long')
