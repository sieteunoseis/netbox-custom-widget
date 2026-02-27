# Changelog

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
