import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("extras", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomAPIEndpoint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Display name for this endpoint",
                        max_length=100,
                        unique=True,
                    ),
                ),
                (
                    "url",
                    models.CharField(
                        help_text="API endpoint URL",
                        max_length=500,
                    ),
                ),
                (
                    "http_method",
                    models.CharField(
                        default="GET",
                        max_length=10,
                    ),
                ),
                (
                    "headers",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="Custom HTTP headers as JSON (e.g., authorization)",
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        blank=True,
                        help_text="Request body for POST requests",
                    ),
                ),
                (
                    "mappings",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="Field mapping configuration as JSON array",
                    ),
                ),
                (
                    "display_mode",
                    models.CharField(
                        default="list",
                        max_length=10,
                    ),
                ),
                (
                    "refresh_interval",
                    models.PositiveIntegerField(
                        default=30,
                        help_text="Auto-refresh interval in seconds (0 to disable)",
                    ),
                ),
                (
                    "verify_ssl",
                    models.BooleanField(
                        default=True,
                        help_text="Verify SSL certificates",
                    ),
                ),
                (
                    "timeout",
                    models.PositiveIntegerField(
                        default=30,
                        help_text="Request timeout in seconds",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True),
                ),
                (
                    "comments",
                    models.TextField(blank=True),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem",
                        to="extras.Tag",
                    ),
                ),
            ],
            options={
                "verbose_name": "API Endpoint",
                "verbose_name_plural": "API Endpoints",
                "ordering": ["name"],
            },
        ),
    ]
