import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("extras", "0001_initial"),
        ("netbox_custom_widget", "0003_increase_url_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookmarkLink",
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
                        help_text="Display name for this bookmark",
                        max_length=200,
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        help_text="Bookmark URL",
                        max_length=500,
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True),
                ),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        help_text="Grouping category (e.g., OHSU Tools, Monitoring)",
                        max_length=100,
                    ),
                ),
                (
                    "icon",
                    models.CharField(
                        blank=True,
                        help_text="MDI icon class (e.g., mdi-help-circle)",
                        max_length=50,
                    ),
                ),
                (
                    "weight",
                    models.PositiveIntegerField(
                        default=100,
                        help_text="Sort order within category (lower = first)",
                    ),
                ),
                (
                    "new_tab",
                    models.BooleanField(
                        default=True,
                        help_text="Open link in new tab",
                    ),
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
                "verbose_name": "Bookmark",
                "verbose_name_plural": "Bookmarks",
                "ordering": ["category", "weight", "name"],
            },
        ),
    ]
