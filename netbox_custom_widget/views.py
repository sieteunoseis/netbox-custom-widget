"""Views for NetBox Custom Widget plugin."""

import logging

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View
from netbox.views import generic

from .filtersets import BookmarkLinkFilterSet, CustomAPIEndpointFilterSet
from .forms import (
    BookmarkLinkBulkEditForm,
    BookmarkLinkFilterForm,
    BookmarkLinkForm,
    BookmarkLinkImportForm,
    CustomAPIEndpointBulkEditForm,
    CustomAPIEndpointFilterForm,
    CustomAPIEndpointForm,
    CustomAPIEndpointImportForm,
)
from .models import BookmarkLink, CustomAPIEndpoint
from .tables import BookmarkLinkTable, CustomAPIEndpointTable
from .utils import fetch_api_data, process_array_mappings, process_mappings

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
        context = {"api_result": result}

        if result["data"] is not None:
            if instance.display_mode == "table" and isinstance(result["data"], list):
                context["table_data"] = process_array_mappings(result["data"], instance.mappings)
            else:
                context["mapped_data"] = process_mappings(result["data"], instance.mappings)
        else:
            context["mapped_data"] = []

        return context


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
# BookmarkLink Views
#


class BookmarkLinkListView(generic.ObjectListView):
    """List view for BookmarkLink objects."""

    queryset = BookmarkLink.objects.prefetch_related("tags")
    table = BookmarkLinkTable
    filterset = BookmarkLinkFilterSet
    filterset_form = BookmarkLinkFilterForm


class BookmarkLinkView(generic.ObjectView):
    """Detail view for BookmarkLink objects."""

    queryset = BookmarkLink.objects.prefetch_related("tags")


class BookmarkLinkEditView(generic.ObjectEditView):
    """Create/Edit view for BookmarkLink objects."""

    queryset = BookmarkLink.objects.all()
    form = BookmarkLinkForm


class BookmarkLinkDeleteView(generic.ObjectDeleteView):
    """Delete view for BookmarkLink objects."""

    queryset = BookmarkLink.objects.all()


class BookmarkLinkBulkImportView(generic.BulkImportView):
    """Bulk import view for BookmarkLink objects."""

    queryset = BookmarkLink.objects.all()
    model_form = BookmarkLinkImportForm


class BookmarkLinkBulkEditView(generic.BulkEditView):
    """Bulk edit view for BookmarkLink objects."""

    queryset = BookmarkLink.objects.prefetch_related("tags")
    filterset = BookmarkLinkFilterSet
    table = BookmarkLinkTable
    form = BookmarkLinkBulkEditForm


class BookmarkLinkBulkDeleteView(generic.BulkDeleteView):
    """Bulk delete view for BookmarkLink objects."""

    queryset = BookmarkLink.objects.all()
    filterset = BookmarkLinkFilterSet
    table = BookmarkLinkTable


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

        context = {"endpoint": endpoint, "error": None}

        if endpoint.display_mode == "table" and isinstance(result["data"], list):
            context["table_data"] = process_array_mappings(result["data"], endpoint.mappings)
        else:
            context["mapped_data"] = process_mappings(result["data"], endpoint.mappings)

        html = render_to_string(
            "netbox_custom_widget/widgets/custom_api_content.html",
            context,
        )
        return HttpResponse(html)
