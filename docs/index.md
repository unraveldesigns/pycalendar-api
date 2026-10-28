# PyCalendar API: Moroccan Holidays & Calendar Client for Python

<figure markdown="span">
    ![Calendar API Logo](assets/img/logo.webp){ width="350" }
  <figcaption>Calendar • API • Holidays • Morocco</figcaption>
</figure>

[![Latest Release](https://gitlab.com/ud-labs/py-calendar-api/-/badges/release.svg)](https://gitlab.com/ud-labs/py-calendar-api/-/releases)
[![PyPI version](https://img.shields.io/pypi/v/pycalendar-api.svg)](https://pypi.org/project/pycalendar-api/)
[![Python versions](https://img.shields.io/pypi/pyversions/pycalendar-api.svg)](https://pypi.org/project/pycalendar-api/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pycalendar-api.svg)](https://pypi.org/project/pycalendar-api/)
[![License](https://img.shields.io/pypi/l/pycalendar-api.svg)](https://pypi.org/project/pycalendar-api/)

**PyCalendar API** is the **official** Python client wrapper for the [Calendar-API.ma](https://calendar-api.ma) platform.
It allows developers to programmatically fetch **Moroccan public holidays**, track **Hijri calendar events**,
and compute local business day data.

Easy and free registration to [Calendar API](https://calendar-api.ma/console/register)

🔗 **Quick Links**: [📝 Register for Free](https://calendar-api.ma/console/register) | [⚡ Live API Docs](https://calendar-api.ma/api/v1/docs) | [💻 Schema OpenAPI 3.1 (JSON)](https://calendar-api.ma/schema/openapi.json) | [🟢 Health Check](https://calendar-api.ma/health)

## ✨ Key Features

- **Moroccan Public Holidays**: Dynamically fetch national, religious, and exceptional holidays.
- **Dual Calendar Support**: Track `Religious` and `Exceptional` holidays for accurate calculation and history sanitization.
- **Business Day Calculations**: Calculate working days, skipping custom weekends and local banking closures.
- **Modern Python Design**: Built with `dataclasses`, fully typed, and automatic JSON-to-Python object conversion.
- **Minimal Dependencies**: Lightweight and fast.
- **Advanced Configuration**: Proxy (and `HTTPS_PROXY`/`NO_PROXY`), timeouts, retries, CA bundles and client certificates, as client arguments or in a `.toml` file.

## 📦 Installation

Install the latest version from PyPI:
```bash
pip install pycalendar-api
```

## Quick Start & Usage Examples

Ensure that you are registered, if not, you can [Register](https://calendar-api.ma/console/register) for free 

Instanciate the API Client by providing one the active API Keys from your console

```python
from pycalendar_api import CalendarApi, to_date  # Util function for date creation

>>> api = CalendarApi('YOUR_API_KEY')
>>> print(api.health())
ApiHealth(api_status="UP", appname="calendar-api", timestamp=datetime.datetime.now())
```

### 🌙 Holidays API

Holidays domain of Calendar API.

- **Check if a date is a holiday**

```python
from pycalendar_api import CalendarApi, to_date

api = CalendarApi('YOUR_API_KEY') # or api = CalendarApi.from_env()

# Check if a date is a Holiday
>>> result = api.holidays.is_holiday(to_date('14/01/2025'))
>>> print(result)
HolidayCheckResult(
    date=datetime.date(2025, 1, 14), is_holiday=True,
    description="Nouvel An Amazigh", holiday_type=<CalHolidayType.NATIONAL: 'National'>,
    status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'
)
```

- **List holidays of a year or many years**

```python
>>> result = api.holidays.year(2025)
>>> print(result)
[
    Holiday(description="Jour de l'AN", day=1, month=1, date=datetime.date(2025, 1, 1), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    Holiday(description="Manifeste de l'Indépendance", day=11, month=1, date=datetime.date(2025, 1, 11), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    Holiday(description="Nouvel An Amazigh", day=14, month=1, date=datetime.date(2025, 1, 14), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    ...,
]

# List Holidays of many years
>>> result = api.holidays.years(list(range(2017, 2027)))
>>> print(result)
[
    Holiday(description="Jour de l'AN", day=1, month=1, date=datetime.date(2025, 1, 1), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    Holiday(description="Manifeste de l'Indépendance", day=11, month=1, date=datetime.date(2025, 1, 11), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    Holiday(description="Nouvel An Amazigh", day=14, month=1, date=datetime.date(2025, 1, 14), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    ...,
]
```

### 🏢 Business Days API

Business days domain of Calendar API.


#### Bdays operations

- **Fetch the next or previous Business day**

```python
# Next Business day
result = api.bdays.next_date(to_date('13/01/2025'))
>>> print(result)
NextDate(date=datetime.date(2025, 1, 13), next_date=datetime.date(2025, 1, 15))

# Previous Business day
result = api.bdays.previous_date(to_date('15/01/2025'))
>>> print(result)
PreviousDate(date=datetime.date(2025, 1, 15), previous_date=datetime.date(2025, 1, 13))
```

- **List Business days of a year or a month**

```python
# Business days of a year
result = api.bdays.bdays_of(2025)
>>> print(result)
DateSeries(
   ref='bdays-2025', min_date='2025-01-02', max_date='2025-12-31', freq=<CalFreq.DAILY: 'D'>, nitems=247,
   serie=SortedSet([datetime.date(2025, 1, 2), datetime.date(2025, 1, 3), datetime.date(2025, 1, 6), ..., datetime.date(2025, 12, 29), datetime.date(2025, 12, 30), datetime.date(2025, 12, 31)])
)

# Business days of a month
result = api.bdays.bdays_of(2025, month=6)
>>> print(result)
DateSeries(
   ref='bdays-2025-06', min_date='2025-06-02', max_date='2025-06-30', freq=<CalFreq.DAILY: 'D'>, nitems=19,
   serie=SortedSet([datetime.date(2025, 6, 2), datetime.date(2025, 6, 3), datetime.date(2025, 6, 4), datetime.date(2025, 6, 5), ..., datetime.date(2025, 6, 25), datetime.date(2025, 6, 26), datetime.date(2025, 6, 30)])
)
```

- **Count or List Business days between 2 dates**

```python
# Count Business days between 2 dates
>>> count = api.bdays.count(to_date('02/01/2025'), to_date('31/12/2025'))
>>> print(count)
DaysCount(start_date=datetime.date(2025, 1, 2), end_date=datetime.date(2025, 12, 31), count=247, freq=<CalFreq.DAILY: 'D'>)

# List Business days between 2 dates
>>> between = api.bdays.between(to_date('02/01/2025'), to_date('31/12/2025'))
>>> print(between)
DateSeries(
   ref='bdays', min_date='2025-01-02', max_date='2025-12-31', freq=<CalFreq.DAILY: 'D'>, nitems=247,
   serie=SortedSet([datetime.date(2025, 1, 2), datetime.date(2025, 1, 3), datetime.date(2025, 1, 6), ..., datetime.date(2025, 12, 29), datetime.date(2025, 12, 30), datetime.date(2025, 12, 31)])
)
```

#### Spans: Start/End of periods

Calculate the interval composed of the start and end dates of a given period. The start and end dates are open business days.

Successive intervals can be linked

```python
# =============== SPANS: Start/End of periods ===============
# Year 2025 span
>>> span_year = api.bdays.span(2025)
>>> print(span_year)
CalSpan(start_date=datetime.date(2024, 12, 31), end_date=datetime.date(2025, 12, 31), year=2025, semester=None, quarter=None, month=None, country_code='MA')

# 1st Semester of year 2025
>>> span_s1 = api.bdays.span(2025, semester=1)
>>> print(span_s1)
CalSpan(start_date=datetime.date(2024, 12, 31), end_date=datetime.date(2025, 6, 30), year=2025, semester=1, quarter=None, month=None, country_code='MA')

# 3rd Quarter of year 2025
>>> span_quarter = api.bdays.span(2025, quarter=3)
>>> print(span_quarter)
CalSpan(start_date=datetime.date(2025, 6, 30), end_date=datetime.date(2025, 9, 30), year=2025, semester=None, quarter=3, month=None, country_code='MA')

# Month 7 of year 2025 (July) 
>>> span_month = api.bdays.span(2025, month=7)
>>> print(span_month)
CalSpan(start_date=datetime.date(2025, 6, 30), end_date=datetime.date(2025, 7, 31), year=2025, semester=None, quarter=None, month=7, country_code='MA')
```

### ⚡ Async Client

`AsyncCalendarApi` exposes the same domains and operations as `CalendarApi`, to be awaited.

```python
import asyncio
from pycalendar_api import AsyncCalendarApi, to_date

async def main():
    async with AsyncCalendarApi.from_env() as api:  # or AsyncCalendarApi('YOUR_API_KEY')
        print(await api.health())
        next_bday, holidays = await asyncio.gather(
            api.bdays.next_date(to_date('17/11/2025')),
            api.holidays.year(2026),
        )

asyncio.run(main())
```

### 🔧 Configuration

Every client accepts the HTTP options as keyword arguments. They override the configuration and work the same on `CalendarApi` and `AsyncCalendarApi`, and with `from_env()` / `from_config_file()`:

```python
from pycalendar_api import CalendarApi

api = CalendarApi(
    'YOUR_API_KEY',
    proxy='http://user:pass@proxy.corp:3128',
    timeout=30,                          # connect timeout, the read timeout defaults to timeout * 5
    verify='/etc/ssl/certs/corp-ca.pem', # CA bundle file or directory (or False to disable the verification)
)

api = CalendarApi.from_env(proxy='http://proxy.corp:3128')
```

| Option | Default | Description |
|---|---|---|
| `proxy` | `None` | Proxy URL. When unset, `HTTPS_PROXY` / `HTTP_PROXY` / `ALL_PROXY` and `NO_PROXY` are used |
| `trust_env` | `True` | Use the proxy and the `SSL_CERT_FILE` / `SSL_CERT_DIR` environment variables |
| `timeout` | `10` | Connect/write/pool timeout in seconds |
| `read_timeout` | `None` | Read timeout in seconds, `timeout * 5` when unset |
| `retries` | `3` | Retries on connection errors |
| `verify` | `True` | Verify the server certificate, or path to a CA bundle |
| `cert` / `cert_key` | `None` | Client certificate and its key (PEM), for mutual TLS |
| `follow_redirects` | `True` | Follow the HTTP redirects |
| `default_encoding` | `"utf-8"` | Encoding of the responses without charset |

The same options can be stored in a `toml` file, in the `[http_client]` section:

```toml
[api]
api_key = "YOUR_API_KEY"

[http_client]
timeout = 30
proxy = "http://proxy.corp:3128"
verify = "/etc/ssl/certs/corp-ca.pem"
```

```python
api = CalendarApi.from_config_file('pycalendar-api.toml')
```

Anything else `httpx` supports can be passed with `client_kwargs`, ie: `CalendarApi('KEY', client_kwargs={'limits': httpx.Limits(max_connections=10)})`.

## 🏷️ Enum Properties

These properties are present in the response objects and can be used as query parameters.

### 🗂️ Holiday Type (`StrEnum`)

A holiday is categorized into one of the following types:

| Value           | Description                                                                   |
| --------------- | ----------------------------------------------------------------------------- |
| **National**    | The date is a national holiday.                                               |
| **Religious**   | The date is a religious holiday (check the status to see if it is confirmed). |
| **Exceptional** | The date is an exceptional or bridge holiday.                                 |

### 🌕 Holiday Status (`StrEnum`)

These statuses apply to religious holidays, which are `Estimated` before moon sighting and change to `Official` once confirmed. 

> 💡 **Tip:** Consider hourly polling for religious holidays marked as `Estimated`.

| Value         | Description                                                  |
| ------------- | ------------------------------------------------------------ |
| **Official**  | The holiday is officially confirmed.                         |
| **Estimated** | The religious holiday is pending moon sighting confirmation. |

## 🛠️ Support

If you encounter any bugs or have questions, we are here to help:

- ✉️ **Email Support**: [support@calendar-api.ma](mailto:support@calendar-api.ma)
- 🐛 **Issue Tracker**: [GitLab Repository Issues](https://gitlab.com/ud-labs/py-calendar-api/-/issues)
- 📝 **Contact Form**: [calendar-api.ma/contacts.html](https://calendar-api.ma/contacts.html)

<script defer src="https://odometer.calendar-api.ma/script.js" data-website-id="3b3a9e56-7e3a-4c20-b6b4-fce013629789" data-tag="docs"></script>
