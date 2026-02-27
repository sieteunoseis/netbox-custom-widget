"""Filtersets for NetBox Custom Widget plugin."""

import django_filters
from netbox.filtersets import NetBoxModelFilterSet

from .models import CustomAPIEndpoint, DisplayModeChoices, HTTPMethodChoices


class CustomAPIEndpointFilterSet(NetBoxModelFilterSet):
    """Filterset for CustomAPIEndpoint model."""

    name = django_filters.CharFilter(lookup_expr="icontains")
    http_method = django_filters.MultipleChoiceFilter(choices=HTTPMethodChoices)
    display_mode = django_filters.MultipleChoiceFilter(choices=DisplayModeChoices)

    class Meta:
        model = CustomAPIEndpoint
        fields = ["id", "name", "http_method", "display_mode"]

    def search(self, queryset, name, value):
        """Search across multiple fields."""
        if not value.strip():
            return queryset
        from django.db.models import Q

        return queryset.filter(Q(name__icontains=value) | Q(url__icontains=value) | Q(description__icontains=value))
