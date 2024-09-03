from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from locations.models import Location
from locations.serializers import LocationSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAdminUser,)
