# Real-Life API Examples

A collection of ready-to-use configurations using **free, public APIs** (no authentication required) to showcase each display mode and color system. Copy any example directly into your `PLUGINS_CONFIG` to try it out.

> **Tip:** You can also create these through the NetBox admin UI at **Plugins > Custom Widget > API Endpoints > Add**.

---

## Table of Contents

- [Block Mode](#block-mode) — Large centered badges for single metrics
- [Grid Mode](#grid-mode) — Side-by-side colored tiles for multi-metric summaries
- [List Mode](#list-mode) — Label/value rows for key-value pairs
- [Table Mode](#table-mode) — Standard tabular layout for structured data
- [Full Dashboard Example](#full-dashboard-example) — Complete `PLUGINS_CONFIG` with multiple widgets

---

## Block Mode

Block mode displays a single large centered badge with a label underneath. Best for KPIs, counters, and single-value metrics.

### Bitcoin Price (CoinDesk API)

Show the current Bitcoin price as a large badge. The CoinDesk API returns live BPI (Bitcoin Price Index) data.

**API:** `https://api.coindesk.com/v1/bpi/currentprice.json`

<details>
<summary>Sample API Response</summary>

```json
{
  "time": {
    "updated": "Feb 28, 2026 12:00:00 UTC",
    "updatedISO": "2026-02-28T12:00:00+00:00"
  },
  "chartName": "Bitcoin",
  "bpi": {
    "USD": {
      "code": "USD",
      "rate": "84,231.45",
      "description": "United States Dollar",
      "rate_float": 84231.45
    },
    "GBP": {
      "code": "GBP",
      "rate": "66,812.30",
      "description": "British Pound Sterling",
      "rate_float": 66812.30
    },
    "EUR": {
      "code": "EUR",
      "rate": "78,544.12",
      "description": "Euro",
      "rate_float": 78544.12
    }
  }
}
```
</details>

```python
{
    'name': 'Bitcoin Price (USD)',
    'url': 'https://api.coindesk.com/v1/bpi/currentprice.json',
    'mappings': [
        {
            'field': 'bpi.USD.rate',
            'label': 'BTC/USD',
            'color': 'warning',
        },
    ],
    'display_mode': 'block',
    'refresh_interval': 60,
    'link': 'https://www.coindesk.com/price/bitcoin/',
}
```

**What it looks like:** A large orange badge showing the current price (e.g., `84,231.45`) with "BTC/USD" label underneath. The widget auto-refreshes every 60 seconds.

---

### GitHub Stars Count (GitHub API)

Display the star count for any GitHub repository as a prominent badge.

**API:** `https://api.github.com/repos/netbox-community/netbox`

<details>
<summary>Sample API Response (abridged)</summary>

```json
{
  "full_name": "netbox-community/netbox",
  "description": "The premier source of truth powering network automation...",
  "stargazers_count": 19902,
  "forks_count": 2951,
  "open_issues_count": 288,
  "subscribers_count": 414,
  "language": "Python"
}
```
</details>

```python
{
    'name': 'NetBox GitHub Stars',
    'url': 'https://api.github.com/repos/netbox-community/netbox',
    'mappings': [
        {
            'field': 'stargazers_count',
            'label': 'GitHub Stars',
            'format': 'number',
            'color': 'warning',
        },
    ],
    'display_mode': 'block',
    'refresh_interval': 300,
    'link': 'https://github.com/netbox-community/netbox',
}
```

**What it looks like:** A large orange badge showing `19,902` with "GitHub Stars" underneath.

---

### NVD Total CVE Count (NIST API)

Show the total number of CVEs tracked by the National Vulnerability Database using threshold coloring.

**API:** `https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=0`

<details>
<summary>Sample API Response</summary>

```json
{
  "resultsPerPage": 0,
  "startIndex": 0,
  "totalResults": 274358,
  "format": "NVD_CVE",
  "version": "2.0",
  "vulnerabilities": []
}
```
</details>

```python
{
    'name': 'NVD CVE Database',
    'url': 'https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=0',
    'mappings': [
        {
            'field': 'totalResults',
            'label': 'Total CVEs Tracked',
            'format': 'number',
            'color': 'danger',
        },
    ],
    'display_mode': 'block',
    'refresh_interval': 3600,
    'link': 'https://nvd.nist.gov/',
}
```

**What it looks like:** A large red badge displaying the total CVE count (e.g., `274,358`) with "Total CVEs Tracked" label. Refreshes hourly.

---

### US Population (REST Countries API)

Display the population of any country as a single metric.

**API:** `https://restcountries.com/v3.1/alpha/US?fields=name,population`

<details>
<summary>Sample API Response</summary>

```json
{
  "name": {
    "common": "United States",
    "official": "United States of America"
  },
  "population": 329484123
}
```
</details>

```python
{
    'name': 'US Population',
    'url': 'https://restcountries.com/v3.1/alpha/US?fields=name,population',
    'mappings': [
        {
            'field': 'population',
            'label': 'United States Population',
            'format': 'number',
            'color': 'primary',
        },
    ],
    'display_mode': 'block',
    'refresh_interval': 86400,
    'link': 'https://restcountries.com/',
}
```

---

## Grid Mode

Grid mode renders colored tiles side-by-side in a responsive row. Best for comparing multiple metrics at a glance — dashboards, summaries, and multi-value overviews.

### GitHub Repository Overview (GitHub API)

Show stars, forks, and open issues as three side-by-side tiles.

**API:** `https://api.github.com/repos/netbox-community/netbox`

```python
{
    'name': 'NetBox GitHub Stats',
    'url': 'https://api.github.com/repos/netbox-community/netbox',
    'mappings': [
        {
            'field': 'stargazers_count',
            'label': 'Stars',
            'format': 'number',
            'color': 'warning',
        },
        {
            'field': 'open_issues_count',
            'label': 'Open Issues',
            'format': 'number',
            'color': 'danger',
        },
        {
            'field': 'forks_count',
            'label': 'Forks',
            'format': 'number',
            'color': 'primary',
        },
    ],
    'display_mode': 'grid',
    'refresh_interval': 300,
    'link': 'https://github.com/netbox-community/netbox',
}
```

**What it looks like:** Three colored tiles in a row — orange `19,902` (Stars), red `288` (Open Issues), blue `2,951` (Forks) — each with its label underneath.

---

### Bitcoin Multi-Currency Price (CoinDesk API)

Show BTC price in USD, GBP, and EUR side-by-side.

**API:** `https://api.coindesk.com/v1/bpi/currentprice.json`

```python
{
    'name': 'Bitcoin Price',
    'url': 'https://api.coindesk.com/v1/bpi/currentprice.json',
    'mappings': [
        {
            'field': 'bpi.USD.rate',
            'label': 'USD',
            'color': 'success',
        },
        {
            'field': 'bpi.GBP.rate',
            'label': 'GBP',
            'color': 'primary',
        },
        {
            'field': 'bpi.EUR.rate',
            'label': 'EUR',
            'color': 'info',
        },
    ],
    'display_mode': 'grid',
    'refresh_interval': 60,
    'link': 'https://www.coindesk.com/price/bitcoin/',
}
```

**What it looks like:** Three tiles — green USD price, blue GBP price, cyan EUR price — showing the live Bitcoin exchange rate in each currency.

---

### Exchange Rates vs USD (ExchangeRate API)

Compare major currency exchange rates in a grid.

**API:** `https://api.exchangerate-api.com/v4/latest/USD`

<details>
<summary>Sample API Response (abridged)</summary>

```json
{
  "provider": "https://www.exchangerate-api.com",
  "base": "USD",
  "rates": {
    "EUR": 0.9234,
    "GBP": 0.7891,
    "JPY": 149.85,
    "CAD": 1.3612,
    "AUD": 1.5432,
    "CHF": 0.8821
  },
  "time_last_updated": 1709136000
}
```
</details>

```python
{
    'name': 'Exchange Rates (USD Base)',
    'url': 'https://api.exchangerate-api.com/v4/latest/USD',
    'mappings': [
        {
            'field': 'rates.EUR',
            'label': 'EUR',
            'color': 'primary',
        },
        {
            'field': 'rates.GBP',
            'label': 'GBP',
            'color': 'success',
        },
        {
            'field': 'rates.JPY',
            'label': 'JPY',
            'color': 'warning',
        },
        {
            'field': 'rates.CAD',
            'label': 'CAD',
            'color': 'danger',
        },
    ],
    'display_mode': 'grid',
    'refresh_interval': 3600,
    'link': 'https://www.exchangerate-api.com/',
}
```

**What it looks like:** Four colored tiles — EUR (blue), GBP (green), JPY (orange), CAD (red) — each displaying the exchange rate against USD.

---

### Weather Conditions (Open-Meteo API)

Display current temperature, wind speed, and humidity as a grid. Open-Meteo requires no API key and provides global weather data.

**API:** `https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current=temperature_2m,wind_speed_10m,relative_humidity_2m&temperature_unit=fahrenheit&wind_speed_unit=mph`

<details>
<summary>Sample API Response</summary>

```json
{
  "latitude": 40.710335,
  "longitude": -73.99307,
  "current": {
    "time": "2026-02-28T12:00",
    "interval": 900,
    "temperature_2m": 42.5,
    "wind_speed_10m": 8.3,
    "relative_humidity_2m": 65
  },
  "current_units": {
    "temperature_2m": "°F",
    "wind_speed_10m": "mp/h",
    "relative_humidity_2m": "%"
  }
}
```
</details>

```python
{
    'name': 'NYC Weather',
    'url': 'https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current=temperature_2m,wind_speed_10m,relative_humidity_2m&temperature_unit=fahrenheit&wind_speed_unit=mph',
    'mappings': [
        {
            'field': 'current.temperature_2m',
            'label': 'Temperature',
            'color': 'danger',
            'suffix': '°F',
        },
        {
            'field': 'current.wind_speed_10m',
            'label': 'Wind Speed',
            'color': 'primary',
            'suffix': 'mph',
        },
        {
            'field': 'current.relative_humidity_2m',
            'label': 'Humidity',
            'color': 'info',
            'suffix': '%',
        },
    ],
    'display_mode': 'grid',
    'refresh_interval': 300,
}
```

**What it looks like:** Three tiles — red temperature (e.g., `42.5 °F`), blue wind speed (e.g., `8.3 mph`), cyan humidity (e.g., `65 %`).

> **Tip:** Change the `latitude` and `longitude` parameters to monitor weather at your data center location.

---

### Crypto Prices with Threshold Colors (CoinGecko API)

Show Bitcoin and Ethereum prices with threshold-based coloring.

**API:** `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd`

<details>
<summary>Sample API Response</summary>

```json
{
  "bitcoin": {
    "usd": 84231.45
  },
  "ethereum": {
    "usd": 3245.67
  }
}
```
</details>

```python
{
    'name': 'Crypto Prices',
    'url': 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd',
    'mappings': [
        {
            'field': 'bitcoin.usd',
            'label': 'Bitcoin',
            'format': 'number',
            'color': 'threshold',
            'suffix': 'USD',
            'thresholds': [
                {'lt': 50000, 'color': 'red'},
                {'lt': 80000, 'color': 'orange'},
                {'color': 'green'},
            ],
        },
        {
            'field': 'ethereum.usd',
            'label': 'Ethereum',
            'format': 'number',
            'color': 'threshold',
            'suffix': 'USD',
            'thresholds': [
                {'lt': 2000, 'color': 'red'},
                {'lt': 3000, 'color': 'orange'},
                {'color': 'green'},
            ],
        },
    ],
    'display_mode': 'grid',
    'refresh_interval': 120,
    'link': 'https://www.coingecko.com/',
}
```

**What it looks like:** Two tiles with dynamic colors — prices below the low threshold turn red, mid-range turns orange, and above the high threshold turns green.

---

## List Mode

List mode renders label/value rows with separators between each item. Best for key-value pairs, status lists, and detail views.

### GitHub Repository Details (GitHub API)

Show detailed repository info as a labeled list.

**API:** `https://api.github.com/repos/netbox-community/netbox`

```python
{
    'name': 'NetBox Repo Details',
    'url': 'https://api.github.com/repos/netbox-community/netbox',
    'mappings': [
        {
            'field': 'language',
            'label': 'Language',
            'color': 'primary',
        },
        {
            'field': 'stargazers_count',
            'label': 'Stars',
            'format': 'number',
            'color': 'warning',
        },
        {
            'field': 'forks_count',
            'label': 'Forks',
            'format': 'number',
            'color': 'info',
        },
        {
            'field': 'open_issues_count',
            'label': 'Open Issues',
            'format': 'number',
            'color': 'threshold',
            'thresholds': [
                {'lt': 100, 'color': 'green'},
                {'lt': 500, 'color': 'orange'},
                {'color': 'red'},
            ],
        },
        {
            'field': 'subscribers_count',
            'label': 'Watchers',
            'format': 'number',
            'color': 'secondary',
        },
        {
            'field': 'default_branch',
            'label': 'Default Branch',
            'color': 'success',
        },
    ],
    'display_mode': 'list',
    'refresh_interval': 600,
    'link': 'https://github.com/netbox-community/netbox',
}
```

**What it looks like:**

```
Language                    Python    (blue badge)
Stars                       19,902   (orange badge)
Forks                        2,951   (cyan badge)
Open Issues                    288   (orange badge, threshold)
Watchers                       414   (muted badge)
Default Branch                main   (green badge)
```

Each row has the label on the left and the colored value badge on the right, with a separator between rows.

---

### Current Time in Multiple Zones (TimeAPI.io)

Show the current time for a specific timezone. Create multiple widgets for different zones.

**API:** `https://timeapi.io/api/time/current/zone?timeZone=America/New_York`

<details>
<summary>Sample API Response</summary>

```json
{
  "year": 2026,
  "month": 2,
  "day": 28,
  "hour": 7,
  "minute": 30,
  "seconds": 16,
  "milliSeconds": 647,
  "dateTime": "2026-02-28T07:30:16.6476606",
  "date": "02/28/2026",
  "time": "07:30",
  "timeZone": "America/New_York",
  "dayOfWeek": "Saturday",
  "dstActive": false
}
```
</details>

```python
{
    'name': 'New York Time',
    'url': 'https://timeapi.io/api/time/current/zone?timeZone=America/New_York',
    'mappings': [
        {
            'field': 'dateTime',
            'label': 'Current Time',
        },
        {
            'field': 'timeZone',
            'label': 'Timezone',
            'color': 'primary',
        },
        {
            'field': 'dayOfWeek',
            'label': 'Day of Week',
            'color': 'info',
        },
        {
            'field': 'dstActive',
            'label': 'DST Active',
            'color': 'secondary',
        },
    ],
    'display_mode': 'list',
    'refresh_interval': 30,
}
```

---

### IP Geolocation Info (ipinfo.io)

Display geolocation data for the NetBox server's public IP.

**API:** `https://ipinfo.io/json`

<details>
<summary>Sample API Response</summary>

```json
{
  "ip": "203.0.113.42",
  "hostname": "server.example.com",
  "city": "San Francisco",
  "region": "California",
  "country": "US",
  "loc": "37.7749,-122.4194",
  "org": "AS13335 Cloudflare, Inc.",
  "postal": "94102",
  "timezone": "America/Los_Angeles"
}
```
</details>

```python
{
    'name': 'Server IP Info',
    'url': 'https://ipinfo.io/json',
    'mappings': [
        {
            'field': 'ip',
            'label': 'Public IP',
            'color': 'primary',
        },
        {
            'field': 'city',
            'label': 'City',
        },
        {
            'field': 'region',
            'label': 'Region',
        },
        {
            'field': 'org',
            'label': 'Organization',
            'color': 'info',
        },
        {
            'field': 'timezone',
            'label': 'Timezone',
            'color': 'secondary',
        },
    ],
    'display_mode': 'list',
    'refresh_interval': 3600,
    'link': 'https://ipinfo.io/',
}
```

---

### Country Details (REST Countries API)

Show detailed information about any country.

**API:** `https://restcountries.com/v3.1/alpha/US?fields=name,capital,population,region,subregion,languages`

<details>
<summary>Sample API Response</summary>

```json
{
  "name": {
    "common": "United States",
    "official": "United States of America"
  },
  "capital": ["Washington, D.C."],
  "population": 329484123,
  "region": "Americas",
  "subregion": "North America",
  "languages": {
    "eng": "English"
  }
}
```
</details>

```python
{
    'name': 'United States Info',
    'url': 'https://restcountries.com/v3.1/alpha/US?fields=name,capital,population,region,subregion',
    'mappings': [
        {
            'field': 'name.official',
            'label': 'Official Name',
        },
        {
            'field': 'capital.0',
            'label': 'Capital',
            'color': 'primary',
        },
        {
            'field': 'population',
            'label': 'Population',
            'format': 'number',
            'color': 'success',
        },
        {
            'field': 'region',
            'label': 'Region',
            'color': 'info',
        },
        {
            'field': 'subregion',
            'label': 'Subregion',
            'color': 'secondary',
        },
    ],
    'display_mode': 'list',
    'refresh_interval': 86400,
    'link': 'https://restcountries.com/',
}
```

---

### Upcoming US Holidays (Nager.Date API)

Show the next upcoming public holiday.

**API:** `https://date.nager.at/api/v3/NextPublicHolidays/US`

<details>
<summary>Sample API Response</summary>

```json
[
  {
    "date": "2026-05-25",
    "localName": "Memorial Day",
    "name": "Memorial Day",
    "countryCode": "US",
    "fixed": false,
    "global": true
  },
  {
    "date": "2026-07-03",
    "localName": "Independence Day",
    "name": "Independence Day",
    "countryCode": "US",
    "fixed": false,
    "global": true
  }
]
```
</details>

```python
{
    'name': 'Next US Holiday',
    'url': 'https://date.nager.at/api/v3/NextPublicHolidays/US',
    'mappings': [
        {
            'field': '0.name',
            'label': 'Holiday',
            'color': 'success',
        },
        {
            'field': '0.date',
            'label': 'Date',
            'color': 'primary',
        },
    ],
    'display_mode': 'list',
    'refresh_interval': 86400,
    'link': 'https://date.nager.at/',
}
```

---

## Table Mode

Table mode renders data in a standard HTML table with headers. Best for structured multi-column data.

### Upcoming Holidays Table (Nager.Date API)

Show the next three US holidays in a table layout.

**API:** `https://date.nager.at/api/v3/NextPublicHolidays/US`

```python
{
    'name': 'Upcoming US Holidays',
    'url': 'https://date.nager.at/api/v3/NextPublicHolidays/US',
    'mappings': [
        {
            'field': '0.name',
            'label': 'Next Holiday',
            'additional_field': '0.date',
            'color': 'success',
        },
        {
            'field': '1.name',
            'label': '2nd Holiday',
            'additional_field': '1.date',
            'color': 'primary',
        },
        {
            'field': '2.name',
            'label': '3rd Holiday',
            'additional_field': '2.date',
            'color': 'info',
        },
    ],
    'display_mode': 'table',
    'refresh_interval': 86400,
    'link': 'https://date.nager.at/',
}
```

**What it looks like:**

| Next Holiday | 2nd Holiday | 3rd Holiday |
|---|---|---|
| Memorial Day | Independence Day | Labor Day |
| 2026-05-25 | 2026-07-03 | 2026-09-07 |

Each value has a colored badge, with the `additional_field` (date) shown below the holiday name.

---

### Multi-City Weather Comparison (Open-Meteo API)

Compare weather across cities. Since each widget calls one endpoint, create a widget per city — or use one endpoint for a single city and show multiple metrics in table format.

**API:** `https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current=temperature_2m,wind_speed_10m,relative_humidity_2m&temperature_unit=fahrenheit&wind_speed_unit=mph`

```python
{
    'name': 'NYC Weather Details',
    'url': 'https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current=temperature_2m,wind_speed_10m,relative_humidity_2m&temperature_unit=fahrenheit&wind_speed_unit=mph',
    'mappings': [
        {
            'field': 'current.temperature_2m',
            'label': 'Temp',
            'color': 'threshold',
            'suffix': '°F',
            'thresholds': [
                {'lt': 32, 'color': 'blue'},
                {'lt': 60, 'color': 'cyan'},
                {'lt': 85, 'color': 'orange'},
                {'color': 'red'},
            ],
        },
        {
            'field': 'current.wind_speed_10m',
            'label': 'Wind',
            'color': 'threshold',
            'suffix': 'mph',
            'thresholds': [
                {'lt': 10, 'color': 'green'},
                {'lt': 25, 'color': 'orange'},
                {'color': 'red'},
            ],
        },
        {
            'field': 'current.relative_humidity_2m',
            'label': 'Humidity',
            'color': 'threshold',
            'suffix': '%',
            'thresholds': [
                {'lt': 30, 'color': 'orange'},
                {'lt': 70, 'color': 'green'},
                {'color': 'blue'},
            ],
        },
    ],
    'display_mode': 'table',
    'refresh_interval': 300,
}
```

**What it looks like:**

| Temp | Wind | Humidity |
|---|---|---|
| 42.5 °F (cyan) | 8.3 mph (green) | 65 % (green) |

Threshold colors change dynamically — freezing temps turn blue, hot temps turn red, high winds turn red, etc.

---

### GitHub Multi-Repo Comparison (GitHub API)

Compare stats for a single repo using table layout with labeled columns.

**API:** `https://api.github.com/repos/netbox-community/netbox`

```python
{
    'name': 'NetBox Repository',
    'url': 'https://api.github.com/repos/netbox-community/netbox',
    'mappings': [
        {
            'field': 'stargazers_count',
            'label': 'Stars',
            'format': 'number',
            'color': 'warning',
        },
        {
            'field': 'forks_count',
            'label': 'Forks',
            'format': 'number',
            'color': 'primary',
        },
        {
            'field': 'open_issues_count',
            'label': 'Issues',
            'format': 'number',
            'color': 'danger',
        },
        {
            'field': 'subscribers_count',
            'label': 'Watchers',
            'format': 'number',
            'color': 'info',
        },
    ],
    'display_mode': 'table',
    'refresh_interval': 600,
    'link': 'https://github.com/netbox-community/netbox',
}
```

---

## Advanced Patterns

### Using `additional_field` for Label + Status Pairs

The `additional_field` option shows two values from the same API response on one row — commonly used to display a name alongside its status. The color is applied to the additional field value.

**API:** `https://date.nager.at/api/v3/NextPublicHolidays/US`

```python
{
    'name': 'Holiday Schedule',
    'url': 'https://date.nager.at/api/v3/NextPublicHolidays/US',
    'mappings': [
        {
            'field': '0.name',
            'label': 'Next',
            'additional_field': '0.date',
            'color': 'success',
        },
        {
            'field': '1.name',
            'label': 'After That',
            'additional_field': '1.date',
            'color': 'primary',
        },
    ],
    'display_mode': 'list',
    'refresh_interval': 86400,
}
```

In **list** mode this renders as:

```
Next        Memorial Day          2026-05-25   (green badge)
After That  Independence Day      2026-07-03   (blue badge)
```

---

### Using POST Requests

Some APIs require POST with a request body. Here's the pattern:

```python
{
    'name': 'POST API Example',
    'url': 'https://httpbin.org/post',
    'http_method': 'POST',
    'headers': {
        'Content-Type': 'application/json',
    },
    'body': '{"query": "test", "limit": 10}',
    'mappings': [
        {
            'field': 'json.query',
            'label': 'Query Echo',
            'color': 'primary',
        },
    ],
    'display_mode': 'list',
    'refresh_interval': 0,
}
```

> **Note:** The `Content-Type: application/json` header is added automatically for POST requests if not specified.

---

### Threshold Color Coding for Monitoring

Thresholds are evaluated top-to-bottom, and the first matching rule wins. The last entry without `lt`/`gt` acts as a default.

```python
# Low is good (e.g., error count, latency)
'thresholds': [
    {'lt': 10, 'color': 'green'},      # < 10: green
    {'lt': 50, 'color': 'orange'},     # < 50: orange
    {'color': 'red'},                  # >= 50: red (default)
]

# High is good (e.g., uptime percentage, success rate)
'thresholds': [
    {'lt': 90, 'color': 'red'},        # < 90%: red
    {'lt': 99, 'color': 'orange'},     # < 99%: orange
    {'color': 'green'},                # >= 99%: green (default)
]

# Range-based (e.g., temperature)
'thresholds': [
    {'lt': 32, 'color': 'blue'},       # Freezing
    {'lt': 60, 'color': 'cyan'},       # Cool
    {'lt': 85, 'color': 'orange'},     # Warm
    {'color': 'red'},                  # Hot
]
```

---

### Customizing Weather Location

Swap coordinates to monitor any location. Here are common data center cities:

| City | Latitude | Longitude |
|------|----------|-----------|
| New York | 40.7128 | -74.0060 |
| San Francisco | 37.7749 | -122.4194 |
| London | 51.5074 | -0.1278 |
| Tokyo | 35.6762 | 139.6503 |
| Frankfurt | 50.1109 | 8.6821 |
| Singapore | 1.3521 | 103.8198 |
| Sydney | -33.8688 | 151.2093 |

Example for Tokyo:
```
https://api.open-meteo.com/v1/forecast?latitude=35.6762&longitude=139.6503&current=temperature_2m,wind_speed_10m,relative_humidity_2m&temperature_unit=fahrenheit&wind_speed_unit=mph
```

---

## Full Dashboard Example

Here's a complete `PLUGINS_CONFIG` that sets up a multi-widget dashboard with a variety of display modes and data sources:

```python
PLUGINS_CONFIG = {
    'netbox_custom_widget': {
        'verify_ssl': True,
        'endpoints': [
            # Block: Bitcoin price as a single large badge
            {
                'name': 'Bitcoin Price (USD)',
                'url': 'https://api.coindesk.com/v1/bpi/currentprice.json',
                'mappings': [
                    {
                        'field': 'bpi.USD.rate',
                        'label': 'BTC/USD',
                        'color': 'warning',
                    },
                ],
                'display_mode': 'block',
                'refresh_interval': 60,
                'link': 'https://www.coindesk.com/price/bitcoin/',
                'description': 'Live Bitcoin price from CoinDesk BPI',
            },
            # Grid: GitHub repo stats side-by-side
            {
                'name': 'NetBox GitHub Stats',
                'url': 'https://api.github.com/repos/netbox-community/netbox',
                'mappings': [
                    {'field': 'stargazers_count', 'label': 'Stars', 'format': 'number', 'color': 'warning'},
                    {'field': 'open_issues_count', 'label': 'Issues', 'format': 'number', 'color': 'danger'},
                    {'field': 'forks_count', 'label': 'Forks', 'format': 'number', 'color': 'primary'},
                ],
                'display_mode': 'grid',
                'refresh_interval': 300,
                'link': 'https://github.com/netbox-community/netbox',
                'description': 'NetBox repository statistics from GitHub',
            },
            # Grid: Weather for your data center
            {
                'name': 'DC Weather (NYC)',
                'url': 'https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current=temperature_2m,wind_speed_10m,relative_humidity_2m&temperature_unit=fahrenheit&wind_speed_unit=mph',
                'mappings': [
                    {'field': 'current.temperature_2m', 'label': 'Temp', 'color': 'danger', 'suffix': '°F'},
                    {'field': 'current.wind_speed_10m', 'label': 'Wind', 'color': 'primary', 'suffix': 'mph'},
                    {'field': 'current.relative_humidity_2m', 'label': 'Humidity', 'color': 'info', 'suffix': '%'},
                ],
                'display_mode': 'grid',
                'refresh_interval': 300,
                'description': 'Current weather at NYC data center',
            },
            # List: Server IP geolocation
            {
                'name': 'Server IP Info',
                'url': 'https://ipinfo.io/json',
                'mappings': [
                    {'field': 'ip', 'label': 'Public IP', 'color': 'primary'},
                    {'field': 'city', 'label': 'City'},
                    {'field': 'region', 'label': 'Region'},
                    {'field': 'org', 'label': 'Organization', 'color': 'info'},
                    {'field': 'timezone', 'label': 'Timezone', 'color': 'secondary'},
                ],
                'display_mode': 'list',
                'refresh_interval': 3600,
                'link': 'https://ipinfo.io/',
                'description': 'Geolocation info for NetBox server public IP',
            },
            # List: Exchange rates
            {
                'name': 'USD Exchange Rates',
                'url': 'https://api.exchangerate-api.com/v4/latest/USD',
                'mappings': [
                    {'field': 'rates.EUR', 'label': 'EUR', 'color': 'primary'},
                    {'field': 'rates.GBP', 'label': 'GBP', 'color': 'success'},
                    {'field': 'rates.JPY', 'label': 'JPY', 'color': 'warning'},
                    {'field': 'rates.CAD', 'label': 'CAD', 'color': 'info'},
                ],
                'display_mode': 'list',
                'refresh_interval': 3600,
                'description': 'Live exchange rates from USD',
            },
            # Table: Upcoming holidays
            {
                'name': 'Upcoming US Holidays',
                'url': 'https://date.nager.at/api/v3/NextPublicHolidays/US',
                'mappings': [
                    {'field': '0.name', 'label': 'Next', 'additional_field': '0.date', 'color': 'success'},
                    {'field': '1.name', 'label': '2nd', 'additional_field': '1.date', 'color': 'primary'},
                    {'field': '2.name', 'label': '3rd', 'additional_field': '2.date', 'color': 'info'},
                ],
                'display_mode': 'table',
                'refresh_interval': 86400,
                'link': 'https://date.nager.at/',
                'description': 'Next three US public holidays',
            },
        ],
    },
}
```

This gives you six widgets covering all four display modes with real data:
1. **Bitcoin Price** — block mode, single large badge
2. **GitHub Stats** — grid mode, three metrics side-by-side
3. **Data Center Weather** — grid mode with suffixes
4. **Server IP Info** — list mode, key-value pairs
5. **Exchange Rates** — list mode with static colors
6. **Upcoming Holidays** — table mode with additional fields

---

## Tips

- **No API key needed** — Every example above uses a free public API with no authentication.
- **Start with block mode** — It's the simplest way to verify your endpoint is working.
- **Use the admin UI** — The endpoint detail page (`/plugins/custom-widget/endpoints/<id>/`) has a live preview to test configurations.
- **Combine widgets** — Add multiple Custom API widgets to your NetBox dashboard to build a monitoring overview.
- **Adjust refresh intervals** — Use lower intervals (5-30s) for real-time monitoring and higher intervals (300-3600s) for slowly changing data.
- **SSL issues?** — Set `'verify_ssl': False` per-endpoint or globally if you're calling internal APIs with self-signed certificates.
