"""Dashboard widgets for the NetBox Custom Widget plugin."""

import logging

from django import forms
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from extras.dashboard.utils import register_widget
from extras.dashboard.widgets import DashboardWidget, WidgetConfigForm

from .models import CustomAPIEndpoint
from .utils import fetch_api_data, process_mappings

logger = logging.getLogger(__name__)


@register_widget
class CustomAPIWidget(DashboardWidget):
    """Dashboard widget that calls an external API and displays results."""

    default_title = _("Custom API")
    description = _("Display data from an external API endpoint.")
    template_name = "netbox_custom_widget/widgets/custom_api.html"
    width = 4
    height = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Auto-set title to endpoint name if using default title
        if self.title == self.default_title:
            endpoint_id = self.config.get("endpoint_id")
            if endpoint_id:
                try:
                    endpoint = CustomAPIEndpoint.objects.get(pk=endpoint_id)
                    self.title = endpoint.name
                except CustomAPIEndpoint.DoesNotExist:
                    pass

    class ConfigForm(WidgetConfigForm):
        endpoint_id = forms.IntegerField(
            label=_("API Endpoint"),
            help_text=_("Select an API endpoint to display."),
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Build choices from available endpoints
            choices = [(None, "---------")]
            try:
                for ep in CustomAPIEndpoint.objects.all().order_by("name"):
                    choices.append((ep.pk, ep.name))
            except Exception:
                pass
            self.fields["endpoint_id"] = forms.TypedChoiceField(
                choices=choices,
                coerce=int,
                label=_("API Endpoint"),
                help_text=_("Select an API endpoint to display."),
            )

    def render(self, request):
        endpoint_id = self.config.get("endpoint_id")
        if not endpoint_id:
            return render_to_string(
                self.template_name,
                {"error": "No endpoint selected. Configure this widget to select an API endpoint."},
            )

        try:
            endpoint = CustomAPIEndpoint.objects.get(pk=endpoint_id)
        except CustomAPIEndpoint.DoesNotExist:
            return render_to_string(
                self.template_name,
                {"error": f"Endpoint ID {endpoint_id} not found."},
            )

        result = fetch_api_data(endpoint)

        if result["error"]:
            return render_to_string(
                self.template_name,
                {
                    "error": result["error"],
                    "endpoint": endpoint,
                },
            )

        mapped_data = process_mappings(result["data"], endpoint.mappings)

        return render_to_string(
            self.template_name,
            {
                "mapped_data": mapped_data,
                "endpoint": endpoint,
                "error": None,
            },
        )
