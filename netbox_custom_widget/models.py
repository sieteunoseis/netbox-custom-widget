"""Models for NetBox Custom Widget plugin."""

from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet


class HTTPMethodChoices(ChoiceSet):
    """HTTP method choices."""

    key = "CustomAPIEndpoint.http_method"

    METHOD_GET = "GET"
    METHOD_POST = "POST"

    CHOICES = [
        (METHOD_GET, "GET", "blue"),
        (METHOD_POST, "POST", "green"),
    ]


class DisplayModeChoices(ChoiceSet):
    """Display mode choices for widget rendering."""

    key = "CustomAPIEndpoint.display_mode"

    MODE_LIST = "list"
    MODE_BLOCK = "block"
    MODE_GRID = "grid"
    MODE_TABLE = "table"

    CHOICES = [
        (MODE_LIST, "List", "blue"),
        (MODE_BLOCK, "Block", "gray"),
        (MODE_GRID, "Grid", "green"),
        (MODE_TABLE, "Table", "purple"),
    ]


class CustomAPIEndpoint(NetBoxModel):
    """
    Stores configuration for an external API endpoint.

    Each endpoint defines a URL, authentication, field mappings,
    and display settings for use in dashboard widgets.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Display name for this endpoint",
    )
    url = models.CharField(
        max_length=500,
        help_text="API endpoint URL",
    )
    http_method = models.CharField(
        max_length=10,
        choices=HTTPMethodChoices,
        default=HTTPMethodChoices.METHOD_GET,
    )
    headers = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom HTTP headers as JSON (e.g., authorization)",
    )
    body = models.TextField(
        blank=True,
        help_text="Request body for POST requests",
    )
    mappings = models.JSONField(
        default=list,
        blank=True,
        help_text="Field mapping configuration as JSON array",
    )
    display_mode = models.CharField(
        max_length=10,
        choices=DisplayModeChoices,
        default=DisplayModeChoices.MODE_LIST,
    )
    refresh_interval = models.PositiveIntegerField(
        default=30,
        help_text="Auto-refresh interval in seconds (0 to disable)",
    )
    verify_ssl = models.BooleanField(
        default=True,
        help_text="Verify SSL certificates",
    )
    timeout = models.PositiveIntegerField(
        default=30,
        help_text="Request timeout in seconds",
    )
    link = models.CharField(
        max_length=500,
        blank=True,
        help_text="Custom URL to link from the widget (opens in new tab)",
    )
    description = models.TextField(
        blank=True,
    )
    comments = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "API Endpoint"
        verbose_name_plural = "API Endpoints"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_custom_widget:customapiendpoint", args=[self.pk])
