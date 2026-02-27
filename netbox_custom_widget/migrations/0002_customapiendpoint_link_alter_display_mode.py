from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_custom_widget", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customapiendpoint",
            name="link",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Custom URL to link from the widget (opens in new tab)",
                max_length=500,
            ),
        ),
    ]
