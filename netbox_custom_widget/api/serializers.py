"""API serializers for NetBox Custom Widget plugin."""

from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ..models import CustomAPIEndpoint


class CustomAPIEndpointSerializer(NetBoxModelSerializer):
    """Serializer for CustomAPIEndpoint."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_custom_widget-api:customapiendpoint-detail"
    )
    endpoint_url = serializers.CharField(source="url", read_only=True)

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
