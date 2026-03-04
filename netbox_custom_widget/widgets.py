"""Dashboard widgets for the NetBox Custom Widget plugin."""

import logging
from itertools import groupby

from django import forms
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from extras.dashboard.utils import register_widget
from extras.dashboard.widgets import DashboardWidget, WidgetConfigForm

from .models import BookmarkLink, CustomAPIEndpoint
from .utils import fetch_api_data, process_array_mappings, process_mappings

logger = logging.getLogger(__name__)

# Special endpoint ID for the built-in Bookmarks widget
BOOKMARKS_ENDPOINT_ID = "bookmarks"


@register_widget
class CustomAPIWidget(DashboardWidget):
    """Dashboard widget that displays data from API endpoints or bookmarks."""

    default_title = _("Custom Widget")
    description = _("Display data from a widget endpoint.")
    template_name = "netbox_custom_widget/widgets/custom_api.html"
    width = 4
    height = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Auto-set title based on selected endpoint
        if self.title == self.default_title:
            endpoint_id = self.config.get("endpoint_id")
            if endpoint_id == BOOKMARKS_ENDPOINT_ID:
                self.title = "Bookmarks"
            elif endpoint_id:
                try:
                    endpoint = CustomAPIEndpoint.objects.get(pk=endpoint_id)
                    self.title = endpoint.name
                except (CustomAPIEndpoint.DoesNotExist, ValueError):
                    pass

    class ConfigForm(WidgetConfigForm):
        endpoint_id = forms.CharField(
            label=_("Widget Endpoint"),
            help_text=_("Select a widget endpoint to display."),
        )
        category = forms.CharField(
            required=False,
            label=_("Category Filter"),
            help_text=_("For Bookmarks only: filter by category name. Leave blank for all."),
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Build choices: API endpoints + Bookmarks
            choices = [("", "---------")]
            try:
                for ep in CustomAPIEndpoint.objects.all().order_by("name"):
                    choices.append((str(ep.pk), ep.name))
            except Exception:
                pass
            choices.append((BOOKMARKS_ENDPOINT_ID, "Bookmarks"))
            self.fields["endpoint_id"] = forms.ChoiceField(
                choices=choices,
                label=_("Widget Endpoint"),
                help_text=_("Select a widget endpoint to display."),
            )

    def render(self, request):
        endpoint_id = self.config.get("endpoint_id")
        if not endpoint_id:
            return render_to_string(
                self.template_name,
                {"error": "No endpoint selected. Configure this widget to select a widget endpoint."},
            )

        # Handle Bookmarks endpoint
        if endpoint_id == BOOKMARKS_ENDPOINT_ID:
            return self._render_bookmarks()

        # Handle API endpoints
        try:
            endpoint = CustomAPIEndpoint.objects.get(pk=int(endpoint_id))
        except (CustomAPIEndpoint.DoesNotExist, ValueError):
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

        context = {"endpoint": endpoint, "error": None}

        if endpoint.display_mode == "table" and isinstance(result["data"], list):
            context["table_data"] = process_array_mappings(result["data"], endpoint.mappings)
        else:
            context["mapped_data"] = process_mappings(result["data"], endpoint.mappings)

        return render_to_string(self.template_name, context)

    def _render_bookmarks(self):
        """Render the bookmarks widget."""
        category = self.config.get("category", "").strip()
        qs = BookmarkLink.objects.order_by("category", "weight", "name")
        if category:
            qs = qs.filter(category__iexact=category)

        grouped = []
        for cat, items in groupby(qs, key=lambda b: b.category or "Uncategorized"):
            grouped.append({"category": cat, "bookmarks": list(items)})

        return render_to_string(
            "netbox_custom_widget/widgets/bookmarks.html",
            {"grouped_bookmarks": grouped},
        )
