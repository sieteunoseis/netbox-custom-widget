"""Utility functions for NetBox Custom Widget plugin."""

import logging

import requests

logger = logging.getLogger(__name__)


def extract_field(data, field_path):
    """
    Extract a value from nested JSON data using dot-notation path.

    Supports:
    - Simple keys: "status" -> data["status"]
    - Nested keys: "data.status" -> data["data"]["status"]
    - Array indices: "0.name" -> data[0]["name"]
    - Mixed: "results.0.status" -> data["results"][0]["status"]

    Returns the extracted value or None if path is invalid.
    """
    if not field_path or data is None:
        return None

    current = data
    for part in field_path.split("."):
        try:
            if isinstance(current, (list, tuple)):
                current = current[int(part)]
            elif isinstance(current, dict):
                if part in current:
                    current = current[part]
                elif part.isdigit():
                    current = current[int(part)]
                else:
                    return None
            else:
                return None
        except (IndexError, KeyError, ValueError, TypeError):
            return None

    return current


def get_adaptive_color(value):
    """
    Determine Bootstrap color class based on status value text.

    Matches Homepage's custom.js UCCE process status coloring.
    """
    if value is None:
        return ""

    val = str(value).lower().strip()

    # Active/Up states -> blue (primary)
    if any(kw in val for kw in ("active", "insvc", "in service")):
        return "badge text-bg-primary"

    # Up/OK/Running -> green (success)
    if any(kw in val for kw in ("up", "ok", "running", "online", "healthy", "on duty")):
        return "badge text-bg-success"

    # Down/Error states -> red (danger)
    if any(kw in val for kw in ("down", "isolated", "error", "failed", "offline", "critical")):
        return "badge text-bg-danger"

    # Warning/Idle states -> orange (warning)
    if any(kw in val for kw in ("standby", "idle", "not active", "configured", "warning", "degraded", "paused")):
        return "badge text-bg-warning"

    return ""


def get_static_color(color_name):
    """Map color name to Bootstrap class."""
    color_map = {
        "success": "badge text-bg-success",
        "warning": "badge text-bg-warning",
        "danger": "badge text-bg-danger",
        "info": "badge text-bg-info",
        "primary": "badge text-bg-primary",
        "secondary": "badge text-bg-secondary",
        "theme": "badge text-bg-primary",
    }
    return color_map.get(color_name, "")


def fetch_api_data(endpoint):
    """
    Make an HTTP request to the configured API endpoint.

    Args:
        endpoint: CustomAPIEndpoint model instance

    Returns:
        dict with keys: data (parsed JSON), error (str or None)
    """
    try:
        kwargs = {
            "headers": endpoint.headers or {},
            "timeout": endpoint.timeout or 30,
            "verify": endpoint.verify_ssl,
        }

        if endpoint.http_method == "POST" and endpoint.body:
            kwargs["data"] = endpoint.body
            if "Content-Type" not in kwargs["headers"]:
                kwargs["headers"]["Content-Type"] = "application/json"

        response = requests.request(
            method=endpoint.http_method,
            url=endpoint.url,
            **kwargs,
        )
        response.raise_for_status()

        return {"data": response.json(), "error": None}

    except requests.exceptions.Timeout:
        return {"data": None, "error": f"Request timed out ({endpoint.timeout}s)"}
    except requests.exceptions.ConnectionError:
        return {"data": None, "error": "Connection failed"}
    except requests.exceptions.HTTPError as e:
        return {"data": None, "error": f"HTTP {e.response.status_code}"}
    except ValueError:
        return {"data": None, "error": "Invalid JSON response"}
    except Exception as e:
        logger.warning(f"API call failed for {endpoint.name}: {e}")
        return {"data": None, "error": str(e)}


def process_mappings(data, mappings):
    """
    Apply field mappings to extracted API data.

    Args:
        data: Parsed JSON response data
        mappings: List of mapping dicts from endpoint config

    Returns:
        List of dicts with keys: label, value, additional_value,
        color_class, suffix, format
    """
    results = []

    for mapping in mappings:
        field_path = mapping.get("field", "")
        value = extract_field(data, field_path)

        # Get additional field if specified
        additional_field = mapping.get("additional_field")
        additional_value = extract_field(data, additional_field) if additional_field else None

        # Determine color class
        color = mapping.get("color", "")
        if color == "adaptive":
            # Apply adaptive coloring to additional_value if present, else value
            color_target = additional_value if additional_value is not None else value
            color_class = get_adaptive_color(color_target)
        elif color:
            color_class = get_static_color(color)
        else:
            color_class = ""

        # Format value
        fmt = mapping.get("format", "text")
        if fmt == "number" and value is not None:
            try:
                value = f"{int(value):,}"
            except (ValueError, TypeError):
                pass

        results.append(
            {
                "label": mapping.get("label", ""),
                "value": value if value is not None else "N/A",
                "additional_value": additional_value,
                "color_class": color_class,
                "suffix": mapping.get("suffix", ""),
                "format": fmt,
            }
        )

    return results
