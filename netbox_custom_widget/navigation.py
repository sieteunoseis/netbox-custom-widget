"""Navigation menu items for NetBox Custom Widget plugin."""

from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

menu = PluginMenu(
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
            ),
        ),
    ),
    icon_class="mdi mdi-api",
)
