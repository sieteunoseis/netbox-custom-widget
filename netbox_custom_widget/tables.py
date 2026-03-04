"""Tables for NetBox Custom Widget plugin."""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from .models import BookmarkLink, CustomAPIEndpoint


class CustomAPIEndpointTable(NetBoxTable):
    """Table for displaying CustomAPIEndpoint objects."""

    name = tables.Column(linkify=True)
    url = tables.TemplateColumn(
        template_code=(
            '<span style="display:inline-block; max-width:400px; overflow:hidden;'
            ' text-overflow:ellipsis; white-space:nowrap;">{{ value }}</span>'
        ),
    )
    http_method = ChoiceFieldColumn()
    display_mode = ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_custom_widget:customapiendpoint_list")

    class Meta(NetBoxTable.Meta):
        model = CustomAPIEndpoint
        fields = (
            "pk",
            "id",
            "name",
            "url",
            "http_method",
            "display_mode",
            "refresh_interval",
            "verify_ssl",
            "timeout",
            "description",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = (
            "name",
            "url",
            "http_method",
            "display_mode",
            "refresh_interval",
        )


class BookmarkLinkTable(NetBoxTable):
    """Table for displaying BookmarkLink objects."""

    name = tables.Column(linkify=True)
    url = tables.TemplateColumn(
        template_code='<a href="{{ value }}" target="_blank">{{ value|truncatechars:60 }}</a>',
    )
    tags = columns.TagColumn(url_name="plugins:netbox_custom_widget:bookmarklink_list")

    class Meta(NetBoxTable.Meta):
        model = BookmarkLink
        fields = (
            "pk",
            "id",
            "name",
            "url",
            "category",
            "icon",
            "weight",
            "new_tab",
            "description",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = (
            "name",
            "url",
            "category",
            "weight",
            "new_tab",
        )
