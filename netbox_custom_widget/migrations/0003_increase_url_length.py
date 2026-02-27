from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_custom_widget", "0002_customapiendpoint_link_alter_display_mode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customapiendpoint",
            name="url",
            field=models.CharField(
                help_text="API endpoint URL",
                max_length=2000,
            ),
        ),
    ]
