"""API serializers for NetBox Custom Widget plugin."""

from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ..models import BookmarkLink, CustomAPIEndpoint


class CustomAPIEndpointSerializer(NetBoxModelSerializer):
    """Serializer for CustomAPIEndpoint."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_custom_widget-api:customapiendpoint-detail"
    )
    endpoint_url = serializers.CharField(source="url")

    class Meta:
        model = CustomAPIEndpoint
        fields = [
            "id",
            "url",
            "display",
            "name",
            "endpoint_url",
            "http_method",
            "headers",
            "body",
            "mappings",
            "display_mode",
            "refresh_interval",
            "link",
            "verify_ssl",
            "timeout",
            "description",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ["id", "url", "display", "name"]


class BookmarkLinkSerializer(NetBoxModelSerializer):
    """Serializer for BookmarkLink."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_custom_widget-api:bookmarklink-detail"
    )
    bookmark_url = serializers.CharField(source="url")

    class Meta:
        model = BookmarkLink
        fields = [
            "id",
            "url",
            "display",
            "name",
            "bookmark_url",
            "description",
            "category",
            "icon",
            "weight",
            "new_tab",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ["id", "url", "display", "name"]
