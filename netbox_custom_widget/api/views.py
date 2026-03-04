"""API views for NetBox Custom Widget plugin."""

from netbox.api.viewsets import NetBoxModelViewSet

from ..filtersets import BookmarkLinkFilterSet, CustomAPIEndpointFilterSet
from ..models import BookmarkLink, CustomAPIEndpoint
from .serializers import BookmarkLinkSerializer, CustomAPIEndpointSerializer


class CustomAPIEndpointViewSet(NetBoxModelViewSet):
    """API viewset for CustomAPIEndpoint objects."""

    queryset = CustomAPIEndpoint.objects.prefetch_related("tags")
    serializer_class = CustomAPIEndpointSerializer
    filterset_class = CustomAPIEndpointFilterSet


class BookmarkLinkViewSet(NetBoxModelViewSet):
    """API viewset for BookmarkLink objects."""

    queryset = BookmarkLink.objects.prefetch_related("tags")
    serializer_class = BookmarkLinkSerializer
    filterset_class = BookmarkLinkFilterSet
