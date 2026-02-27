# NetBox Custom Widget

A NetBox plugin that provides configurable dashboard widgets for calling external APIs and displaying results. Similar to [Homepage's](https://gethomepage.dev/) Custom API widget.

## Features

- Call any HTTP API endpoint (GET/POST) and display JSON results on your NetBox dashboard
- Configurable field mappings with dot-notation for nested JSON access
- Auto-refresh via HTMX at configurable intervals
- Multiple display modes: **list**, **block**, **grid**, **table**
- Three color systems: **adaptive** (keyword-based), **static** (fixed), **threshold** (numeric ranges)
- Pre-define endpoints in plugin configuration for automatic provisioning
- Full CRUD interface for managing API endpoints
- Custom link button on each widget

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
                'link': 'https://api.example.com/dashboard',
            },
        ],
    }
}
```

## Display Modes

| Mode | Description | Best For |
|------|-------------|----------|
| `list` | Label on left, value/badge on right | Process status, key-value pairs |
| `block` | Large centered badge with label below | Single metrics, ticket counts |
| `grid` | PRTG-style badges side-by-side | Multi-metric summaries |
| `table` | Standard table layout | Tabular data |

## Color Options

### Adaptive (`"color": "adaptive"`)

Automatically colors based on keywords in the value text:

| Keywords | Color |
|----------|-------|
| active, insvc, in service | Blue |
| up, ok, running, online, healthy, on duty | Green |
| down, isolated, error, failed, offline, critical | Red |
| standby, idle, not active, configured, warning, degraded, paused | Orange |

### Static (`"color": "<name>"`)

Fixed color applied to the field. Available names: `success` (green), `warning` (orange), `danger` (red), `info` (cyan), `primary` (blue), `secondary` (muted).

### Threshold (`"color": "threshold"`)

Numeric range-based coloring. Rules are evaluated top-to-bottom, first match wins:

```python
{
    'field': 'ticket_count',
    'label': 'Open Tickets',
    'color': 'threshold',
    'thresholds': [
        {'lt': 5, 'color': 'green'},    # < 5: green
        {'lt': 15, 'color': 'orange'},   # < 15: orange
        {'color': 'red'},                # default: red
    ],
}
```

Supports `lt` (less than) and `gt` (greater than). Available colors: `red`, `orange`, `green`, `blue`, `cyan`, `purple`, `yellow`.

## Mapping Options

Each mapping in the `mappings` array supports:

| Key | Type | Description |
|-----|------|-------------|
| `field` | string | **Required.** Dot-notation path to JSON value (e.g., `"data.status"`, `"0.name"`) |
| `label` | string | Display label |
| `additional_field` | string | Second field shown on same row |
| `color` | string | `"adaptive"`, `"threshold"`, or a static color name |
| `thresholds` | array | Threshold rules (when `color` is `"threshold"`) |
| `format` | string | `"text"` (default) or `"number"` (adds comma separators) |
| `suffix` | string | Appended text (e.g., `"hours"`, `"ms"`) |

## Endpoint Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | | **Required.** Display name (also used as widget title) |
| `url` | string | | **Required.** API endpoint URL (max 2000 chars) |
| `http_method` | string | `GET` | `GET` or `POST` |
| `headers` | dict | `{}` | Custom HTTP headers |
| `body` | string | `""` | Request body (POST only) |
| `mappings` | array | `[]` | Field mapping configuration |
| `display_mode` | string | `list` | `list`, `block`, `grid`, or `table` |
| `refresh_interval` | int | `30` | Auto-refresh seconds (0 to disable) |
| `verify_ssl` | bool | `true` | Verify SSL certificates |
| `timeout` | int | `30` | Request timeout seconds |
| `link` | string | `""` | Custom URL button on widget |
| `description` | string | `""` | Optional notes |

## Examples

### Single Number Widget (Block Mode)

Display a single metric as a large centered badge — ideal for ticket counts, sensor totals, or any numeric KPI:

```python
{
    'name': 'JIRA Open Tickets',
    'url': 'https://api.example.com/tickets/count',
    'headers': {'Authorization': 'Bearer token123'},
    'mappings': [
        {
            'field': 'total',
            'label': 'Open Tickets',
            'color': 'threshold',
            'thresholds': [
                {'lt': 5, 'color': 'green'},
                {'lt': 15, 'color': 'orange'},
                {'color': 'red'},
            ],
        },
    ],
    'display_mode': 'block',
    'refresh_interval': 30,
    'link': 'https://jira.example.com/dashboard',
}
```

This renders a large color-coded badge with the count, and "Open Tickets" label underneath. The widget title auto-populates from the endpoint name.

### Multi-Metric Summary (Grid Mode)

Display multiple counts side-by-side with PRTG-style badges:

```python
{
    'name': 'Ticket Summary',
    'url': 'https://api.example.com/tickets/summary',
    'mappings': [
        {'field': 'total', 'label': 'Total', 'color': 'threshold',
         'thresholds': [{'lt': 5, 'color': 'green'}, {'lt': 15, 'color': 'orange'}, {'color': 'red'}]},
        {'field': 'in_progress', 'label': 'In Progress', 'color': 'primary'},
        {'field': 'waiting', 'label': 'Waiting', 'color': 'warning'},
    ],
    'display_mode': 'grid',
    'refresh_interval': 60,
}
```

### Process Status Monitoring (List Mode)

Monitor services with adaptive color coding:

```python
{
    'name': 'Server Processes',
    'url': 'https://api.example.com/processes',
    'mappings': [
        {'field': '0.name', 'additional_field': '0.status', 'color': 'adaptive'},
        {'field': '1.name', 'additional_field': '1.status', 'color': 'adaptive'},
    ],
    'display_mode': 'list',
    'refresh_interval': 5,
}
```

Status values like "Active", "Running", "Down", or "Standby" are automatically color-coded.

### Public API Demo (No Auth Required)

Try these examples out of the box to test the plugin:

```python
# NVD CVE Database — large badge with total CVE count
{
    'name': 'NVD CVE Database',
    'url': 'https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=0',
    'mappings': [
        {'field': 'totalResults', 'label': 'Total CVEs', 'format': 'number', 'color': 'danger'},
    ],
    'display_mode': 'block',
    'refresh_interval': 3600,
    'link': 'https://nvd.nist.gov/',
}

# GitHub Repo Stats — stars, issues, forks side-by-side
{
    'name': 'NetBox GitHub',
    'url': 'https://api.github.com/repos/netbox-community/netbox',
    'mappings': [
        {'field': 'stargazers_count', 'label': 'Stars', 'format': 'number', 'color': 'warning'},
        {'field': 'open_issues_count', 'label': 'Issues', 'format': 'number', 'color': 'danger'},
        {'field': 'forks_count', 'label': 'Forks', 'format': 'number', 'color': 'primary'},
    ],
    'display_mode': 'grid',
    'refresh_interval': 300,
    'link': 'https://github.com/netbox-community/netbox',
}
```

## Requirements

- NetBox >= 4.0.0
- Python >= 3.10
