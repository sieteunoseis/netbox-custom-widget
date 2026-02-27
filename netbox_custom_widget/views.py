"""Views for NetBox Custom Widget plugin."""

import logging

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View
from netbox.views import generic

from .filtersets import CustomAPIEndpointFilterSet
from .forms import (
    CustomAPIEndpointBulkEditForm,
    CustomAPIEndpointFilterForm,
    CustomAPIEndpointForm,
    CustomAPIEndpointImportForm,
)
from .models import CustomAPIEndpoint
from .tables import CustomAPIEndpointTable
from .utils import fetch_api_data, process_mappings

logger = logging.getLogger(__name__)


#
# CustomAPIEndpoint Views
#


class CustomAPIEndpointListView(generic.ObjectListView):
    """List view for CustomAPIEndpoint objects."""

    queryset = CustomAPIEndpoint.objects.prefetch_related("tags")
    table = CustomAPIEndpointTable
    filterset = CustomAPIEndpointFilterSet
    filterset_form = CustomAPIEndpointFilterForm


class CustomAPIEndpointView(generic.ObjectView):
    """Detail view for CustomAPIEndpoint objects."""

    queryset = CustomAPIEndpoint.objects.prefetch_related("tags")

    def get_extra_context(self, request, instance):
        # Fetch live data for preview
        result = fetch_api_data(instance)
        mapped_data = []
        if result["data"] is not None:
            mapped_data = process_mappings(result["data"], instance.mappings)

        return {
            "api_result": result,
            "mapped_data": mapped_data,
        }


class CustomAPIEndpointEditView(generic.ObjectEditView):
    """Create/Edit view for CustomAPIEndpoint objects."""

    queryset = CustomAPIEndpoint.objects.all()
    form = CustomAPIEndpointForm


class CustomAPIEndpointDeleteView(generic.ObjectDeleteView):
    """Delete view for CustomAPIEndpoint objects."""

    queryset = CustomAPIEndpoint.objects.all()


class CustomAPIEndpointBulkImportView(generic.BulkImportView):
    """Bulk import view for CustomAPIEndpoint objects."""

    queryset = CustomAPIEndpoint.objects.all()
    model_form = CustomAPIEndpointImportForm


class CustomAPIEndpointBulkEditView(generic.BulkEditView):
    """Bulk edit view for CustomAPIEndpoint objects."""

    queryset = CustomAPIEndpoint.objects.prefetch_related("tags")
    filterset = CustomAPIEndpointFilterSet
    table = CustomAPIEndpointTable
    form = CustomAPIEndpointBulkEditForm


class CustomAPIEndpointBulkDeleteView(generic.BulkDeleteView):
    """Bulk delete view for CustomAPIEndpoint objects."""

    queryset = CustomAPIEndpoint.objects.all()
    filterset = CustomAPIEndpointFilterSet
    table = CustomAPIEndpointTable


#
# Widget HTMX refresh view
#


class WidgetRefreshView(View):
    """HTMX view that returns refreshed widget content for a given endpoint."""

    def get(self, request, pk):
        try:
            endpoint = CustomAPIEndpoint.objects.get(pk=pk)
        except CustomAPIEndpoint.DoesNotExist:
            return HttpResponse('<span class="text-danger">Endpoint not found</span>')

        result = fetch_api_data(endpoint)

        if result["error"]:
            html = render_to_string(
                "netbox_custom_widget/widgets/custom_api_content.html",
                {"error": result["error"], "endpoint": endpoint},
            )
            return HttpResponse(html)

        mapped_data = process_mappings(result["data"], endpoint.mappings)

        html = render_to_string(
            "netbox_custom_widget/widgets/custom_api_content.html",
            {
                "mapped_data": mapped_data,
                "endpoint": endpoint,
                "error": None,
            },
        )
        return HttpResponse(html)
