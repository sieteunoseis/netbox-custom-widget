"""API views for NetBox Custom Widget plugin."""

from netbox.api.viewsets import NetBoxModelViewSet

from ..filtersets import CustomAPIEndpointFilterSet
from ..models import CustomAPIEndpoint
from .serializers import CustomAPIEndpointSerializer


class CustomAPIEndpointViewSet(NetBoxModelViewSet):
    """API viewset for CustomAPIEndpoint objects."""

    queryset = CustomAPIEndpoint.objects.prefetch_related("tags")
    serializer_class = CustomAPIEndpointSerializer
    filterset_class = CustomAPIEndpointFilterSet
