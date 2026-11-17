"""Navigation menu items for NetBox Custom Widget plugin."""

from django.conf import settings
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

_menu = PluginMenu(
    label="Custom Widget",
    groups=(
        (
            "Custom Widget",
            (
                PluginMenuItem(
                    link="plugins:netbox_custom_widget:customapiendpoint_list",
                    link_text="API Endpoints",
                    permissions=["netbox_custom_widget.view_customapiendpoint"],
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_custom_widget:customapiendpoint_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            permissions=["netbox_custom_widget.add_customapiendpoint"],
                        ),
                    ),
                ),
                PluginMenuItem(
                    link="plugins:netbox_custom_widget:bookmarklink_list",
                    link_text="Bookmarks",
                    permissions=["netbox_custom_widget.view_bookmarklink"],
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_custom_widget:bookmarklink_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            permissions=["netbox_custom_widget.add_bookmarklink"],
                        ),
                    ),
                ),
            ),
        ),
    ),
    icon_class="mdi mdi-api",
)


# top_level_menu=False puts this plugin's items under the shared "Plugins" menu
# (grouped by plugin name) instead of its own top-level sidebar menu.
if settings.PLUGINS_CONFIG.get("netbox_custom_widget", {}).get("top_level_menu", True):
    menu = _menu
else:
    menu_items = tuple(item for group in _menu.groups for item in group.items)
