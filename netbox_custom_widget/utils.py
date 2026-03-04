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

    # Active/Up states -> blue
    if any(kw in val for kw in ("active", "insvc", "in service")):
        return "badge text-bg-blue"

    # Up/OK/Running -> green
    if any(kw in val for kw in ("up", "ok", "running", "online", "healthy", "on duty")):
        return "badge text-bg-green"

    # Down/Error states -> red
    if any(kw in val for kw in ("down", "isolated", "error", "failed", "offline", "critical")):
        return "badge text-bg-red"

    # Warning/Idle states -> orange
    if any(kw in val for kw in ("standby", "idle", "not active", "configured", "warning", "degraded", "paused")):
        return "badge text-bg-orange"

    return ""


def get_threshold_color(value, thresholds):
    """
    Determine color based on numeric thresholds.

    Thresholds are evaluated top-to-bottom. Each entry can have:
    - "lt": value less than this number
    - "gt": value greater than this number
    - "color": Tabler color name (red, orange, green, blue, cyan)

    The last entry without lt/gt acts as the default.

    Example:
        [{"lt": 5, "color": "red"}, {"lt": 10, "color": "orange"}, {"color": "green"}]
        -> value < 5: red, value < 10: orange, else: green
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        return ""

    for rule in thresholds:
        color = rule.get("color", "")
        badge = f"badge text-bg-{color}" if color else ""

        if "lt" in rule and num < rule["lt"]:
            return badge
        elif "gt" in rule and num > rule["gt"]:
            return badge
        elif "lt" not in rule and "gt" not in rule:
            return badge

    return ""


def get_static_color(color_name):
    """Map color name to Bootstrap class."""
    color_map = {
        "success": "badge text-bg-green",
        "warning": "badge text-bg-orange",
        "danger": "badge text-bg-red",
        "info": "badge text-bg-cyan",
        "primary": "badge text-bg-blue",
        "secondary": "badge text-bg-muted",
        "theme": "badge text-bg-blue",
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


def format_duration(value):
    """
    Convert a duration value to human-readable format (e.g., "7d 18h 25m").

    Detects and handles multiple input formats:
    - .NET TimeSpan: "7.18:25:31.4904775" (days.HH:mm:ss.fractional)
    - HH:MM:SS: "18:25:31"
    - Seconds (int/float): 640531 or "640531"
    - Milliseconds: 640531000 (auto-detected when > 100000000)
    - ISO 8601 duration: "P7DT18H25M31S" or "PT18H25M"
    - Human-readable: "7 days 18 hours" (returned as-is)

    Returns formatted string or original value if format not recognized.
    """
    import re

    s = str(value).strip()

    # ISO 8601 duration: P[nD]T[nH][nM][nS]
    iso_match = re.match(r"^P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?$", s, re.IGNORECASE)
    if iso_match:
        days = int(iso_match.group(1) or 0)
        hours = int(iso_match.group(2) or 0)
        minutes = int(iso_match.group(3) or 0)
        pieces = []
        if days > 0:
            pieces.append(f"{days}d")
        if hours > 0:
            pieces.append(f"{hours}h")
        if minutes > 0:
            pieces.append(f"{minutes}m")
        return " ".join(pieces) if pieces else "0m"

    # .NET TimeSpan or HH:MM:SS variants
    if ":" in s:
        try:
            days = 0
            time_str = s
            # .NET format: days before first dot if dot comes before colon
            if "." in s.split(":")[0]:
                day_part, time_str = s.split(".", 1)
                days = int(day_part)
            # Strip fractional seconds
            time_part = time_str.split(".")[0] if "." in time_str else time_str
            parts = time_part.split(":")
            hours = int(parts[0]) if len(parts) > 0 else 0
            minutes = int(parts[1]) if len(parts) > 1 else 0

            pieces = []
            if days > 0:
                pieces.append(f"{days}d")
            if hours > 0:
                pieces.append(f"{hours}h")
            if minutes > 0:
                pieces.append(f"{minutes}m")
            return " ".join(pieces) if pieces else "0m"
        except (ValueError, IndexError):
            return s

    # Numeric seconds or milliseconds
    try:
        num = float(s)
        # Heuristic: values > 100M are likely milliseconds
        if num > 100_000_000:
            num = num / 1000
        total_seconds = int(num)
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60

        pieces = []
        if days > 0:
            pieces.append(f"{days}d")
        if hours > 0:
            pieces.append(f"{hours}h")
        if minutes > 0:
            pieces.append(f"{minutes}m")
        if not pieces:
            return f"{total_seconds}s"
        return " ".join(pieces)
    except (ValueError, TypeError):
        pass

    # Already human-readable or unrecognized — return as-is
    return s


def format_value(value, fmt):
    """
    Format a value based on the format type.

    Supported formats:
    - "text": No formatting (default)
    - "number": Comma-separated integers (e.g., 1,234)
    - "duration": Auto-detects time format and converts to "Xd Xh Xm"
    """
    if value is None:
        return value

    if fmt == "number":
        try:
            return f"{int(value):,}"
        except (ValueError, TypeError):
            return value

    if fmt == "duration":
        return format_duration(value)

    return value


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
        elif color == "threshold":
            thresholds = mapping.get("thresholds", [])
            color_target = additional_value if additional_value is not None else value
            color_class = get_threshold_color(color_target, thresholds)
        elif color:
            color_class = get_static_color(color)
        else:
            color_class = ""

        # Format value
        fmt = mapping.get("format", "text")
        value = format_value(value, fmt)

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


def process_array_mappings(data, mappings):
    """
    Process an array of objects into table rows using mappings as column definitions.

    When the API returns a list of objects and display_mode is "table", each mapping
    defines a column. The "field" key is a path within each array item.

    Args:
        data: List of dicts from API response
        mappings: List of mapping dicts (each defines a column)

    Returns:
        dict with "headers" (list of str) and "rows" (list of lists of cell dicts)
    """
    headers = []
    for i, m in enumerate(mappings):
        headers.append(m.get("label") or m.get("field", f"Column {i + 1}"))

    rows = []
    for item in data:
        row = []
        for mapping in mappings:
            field_path = mapping.get("field", "")
            value = extract_field(item, field_path)

            # Color determination
            color = mapping.get("color", "")
            if color == "adaptive":
                color_class = get_adaptive_color(value)
            elif color == "threshold":
                color_class = get_threshold_color(value, mapping.get("thresholds", []))
            elif color:
                color_class = get_static_color(color)
            else:
                color_class = ""

            # Format value
            fmt = mapping.get("format", "text")
            value = format_value(value, fmt)

            row.append(
                {
                    "value": value if value is not None else "N/A",
                    "color_class": color_class,
                    "suffix": mapping.get("suffix", ""),
                }
            )
        rows.append(row)

    return {"headers": headers, "rows": rows}
