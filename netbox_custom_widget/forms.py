"""Forms for NetBox Custom Widget plugin."""

from django import forms
from netbox.forms import NetBoxModelBulkEditForm, NetBoxModelFilterSetForm, NetBoxModelForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, TagFilterField
from utilities.forms.rendering import FieldSet

from .models import CustomAPIEndpoint, DisplayModeChoices, HTTPMethodChoices


class CustomAPIEndpointForm(NetBoxModelForm):
    """Form for creating/editing CustomAPIEndpoint objects."""

    comments = CommentField()

    fieldsets = (
        FieldSet("name", "description", name="General"),
        FieldSet("url", "http_method", "headers", "body", "verify_ssl", "timeout", name="API Configuration"),
        FieldSet("mappings", "display_mode", "refresh_interval", name="Display"),
        FieldSet("comments", "tags", name="Details"),
    )

    class Meta:
        model = CustomAPIEndpoint
        fields = [
            "name",
            "url",
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
        ]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3}),
        }


class CustomAPIEndpointFilterForm(NetBoxModelFilterSetForm):
    """Filter form for CustomAPIEndpoint list view."""

    model = CustomAPIEndpoint

    name = forms.CharField(required=False)
    http_method = forms.MultipleChoiceField(choices=HTTPMethodChoices, required=False)
    display_mode = forms.MultipleChoiceField(choices=DisplayModeChoices, required=False)
    tag = TagFilterField(model)


class CustomAPIEndpointImportForm(NetBoxModelImportForm):
    """Import form for CustomAPIEndpoint objects."""

    class Meta:
        model = CustomAPIEndpoint
        fields = [
            "name",
            "url",
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
        ]


class CustomAPIEndpointBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit form for CustomAPIEndpoint objects."""

    model = CustomAPIEndpoint

    http_method = forms.ChoiceField(choices=HTTPMethodChoices, required=False)
    display_mode = forms.ChoiceField(choices=DisplayModeChoices, required=False)
    refresh_interval = forms.IntegerField(required=False)
    verify_ssl = forms.NullBooleanField(required=False)
    timeout = forms.IntegerField(required=False)
    description = forms.CharField(max_length=200, required=False)
    comments = CommentField()

    nullable_fields = ["description", "comments", "body"]
