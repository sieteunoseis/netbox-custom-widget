"""
NetBox Custom Widget Plugin

Configurable dashboard widgets for calling external APIs and displaying results.
"""

import logging

from django.conf import settings
from django.db.models.signals import post_migrate
from netbox.plugins import PluginConfig

__version__ = "0.2.0"

logger = logging.getLogger(__name__)


def provision_endpoints(sender, **kwargs):
    """Create or update CustomAPIEndpoint objects from plugin configuration."""
    if sender.name != "netbox_custom_widget":
        return

    from django.db import OperationalError, ProgrammingError

    try:
        from .models import CustomAPIEndpoint

        config = settings.PLUGINS_CONFIG.get("netbox_custom_widget", {})
        endpoints_config = config.get("endpoints", [])
        global_verify_ssl = config.get("verify_ssl", True)

        for ep_config in endpoints_config:
            name = ep_config.get("name")
            if not name:
                logger.warning("Skipping endpoint config without 'name'")
                continue

            defaults = {
                "url": ep_config.get("url", ""),
                "http_method": ep_config.get("http_method", "GET"),
                "headers": ep_config.get("headers", {}),
                "body": ep_config.get("body", ""),
                "mappings": ep_config.get("mappings", []),
                "display_mode": ep_config.get("display_mode", "list"),
                "refresh_interval": ep_config.get("refresh_interval", 30),
                "verify_ssl": ep_config.get("verify_ssl", global_verify_ssl),
                "timeout": ep_config.get("timeout", 30),
                "link": ep_config.get("link", ""),
                "description": ep_config.get("description", ""),
            }

            obj, created = CustomAPIEndpoint.objects.update_or_create(
                name=name,
                defaults=defaults,
            )

            if created:
                logger.info(f"Created API endpoint: {name}")
            else:
                logger.debug(f"Updated API endpoint: {name}")

    except (OperationalError, ProgrammingError):
        pass
    except Exception as e:
        logger.warning(f"Could not provision endpoints: {e}")


class CustomWidgetConfig(PluginConfig):
    """Plugin configuration for NetBox Custom Widget."""

    name = "netbox_custom_widget"
    verbose_name = "Custom Widget"
    description = "Configurable dashboard widgets for calling external APIs"
    version = __version__
    author = "Jeremy Worden"
    author_email = "jeremy.worden@gmail.com"
    base_url = "custom-widget"
    min_version = "4.0.0"

    required_settings = []

    default_settings = {
        "verify_ssl": True,
        "endpoints": [],
    }

    def ready(self):
        """Register signal and import widgets."""
        super().ready()
        post_migrate.connect(provision_endpoints, sender=self)
        from . import widgets  # noqa: F401


config = CustomWidgetConfig
