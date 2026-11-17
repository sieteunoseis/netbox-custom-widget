# Changelog

## [0.8.1] - 2026-11-17

### Fixed
- flake8 CI failure (F401 unused json import in utils.py)

## [0.8.0] - 2026-11-17

### Added
- `top_level_menu` setting (default `True`); set `False` to list this plugin's menu items under the shared "Plugins" menu instead of its own top-level sidebar menu

## [0.2.0] - 2026-02-27

### Added
- **Grid display mode** - colored tiles in a responsive grid, ideal for status dashboards
- **Table display mode** - proper HTML table with column headers for structured data
- **Link field** - optional custom URL shown as a button in the widget footer (opens in new tab)
- Link field support in config-based endpoint provisioning

## [0.1.0] - 2026-02-27

### Added
- Initial release
- `CustomAPIEndpoint` model for storing API configurations
- `CustomAPIWidget` dashboard widget with auto-refresh via HTMX
- Adaptive color coding for status values
- Config-based endpoint provisioning via `post_migrate` signal
- Full CRUD views for managing endpoints
- REST API for endpoint management
