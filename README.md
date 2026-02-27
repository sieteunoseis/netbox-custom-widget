# NetBox Custom Widget

A NetBox plugin that provides configurable dashboard widgets for calling external APIs and displaying results. Similar to Homepage's Custom API widget.

## Features

- Call any HTTP API endpoint and display JSON results on your NetBox dashboard
- Configurable field mappings with dot-notation for nested JSON access
- Auto-refresh via HTMX at configurable intervals
- Adaptive color coding for status values (e.g., UCCE process monitoring)
- Pre-define endpoints in plugin configuration for automatic provisioning
- Full CRUD interface for managing API endpoints

## Installation

```bash
pip install netbox-custom-widget
```

Add to your NetBox configuration:

```python
PLUGINS = ['netbox_custom_widget']
```

## Configuration

Define API endpoints in your `plugins.py`:

```python
PLUGINS_CONFIG = {
    'netbox_custom_widget': {
        'verify_ssl': False,
        'endpoints': [
            {
                'name': 'My API Status',
                'url': 'https://api.example.com/status',
                'headers': {'Authorization': 'Bearer token123'},
                'mappings': [
                    {'field': 'status', 'label': 'Status', 'color': 'adaptive'},
                    {'field': 'uptime', 'label': 'Uptime', 'suffix': 'hours'},
                ],
                'display_mode': 'list',
                'refresh_interval': 30,
            },
        ],
    }
}
```

## Requirements

- NetBox >= 4.0.0
- Python >= 3.10
