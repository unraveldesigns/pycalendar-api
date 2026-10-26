# PyCalendar API: Official Python Client for Moroccan Holidays & Business Days

[![Release](https://gitlab.com/ud-labs/py-calendar-api/-/badges/release.svg)](https://gitlab.com/ud-labs/py-calendar-api/-/releases)
[![PyPI version](https://img.shields.io/pypi/v/pycalendar-api.svg)](https://pypi.org/project/pycalendar-api/)
[![Python versions](https://img.shields.io/pypi/pyversions/pycalendar-api.svg)](https://pypi.org/project/pycalendar-api/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pycalendar-api.svg)](https://pypi.org/project/pycalendar-api/)
[![License](https://img.shields.io/pypi/l/pycalendar-api.svg)](https://pypi.org/project/pycalendar-api/)

**PyCalendar API** is the **official**, fully-typed Python client wrapper for the [Calendar-API.ma](https://calendar-api.ma) platform. It allows developers to programmatically fetch Moroccan public holidays, track Hijri calendar events, and compute local business day data with minimal dependencies.

🔗 **Quick Links**: [📝 Register for Free](https://calendar-api.ma/console/register) | [📚 Documentation](https://docs.calendar-api.ma) | [⚡ Live API Docs](https://calendar-api.ma/api/v1/docs) | [🟢 Health Check](https://calendar-api.ma/health)

## 📑 Table of Contents

- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
  - [Authentication](#authentication)
  - [Holidays API](#holidays-api)
  - [Business Days API](#business-days-api)
  - [Period Spans](#period-spans)
  - [Async Client](#-async-client)
- [Enum Properties](#-enum-properties)
- [Support](#-support)

## ✨ Key Features

- **Moroccan Public Holidays**: Dynamically fetch national, religious, and exceptional holidays.
- **Dual Calendar Support**: Track `Religious` and `Exceptional` holidays for accurate calculation and history sanitization.
- **Business Day Calculations**: Calculate working days, skipping custom weekends and local banking closures.
- **Modern Python Design**: Built with `dataclasses`, fully typed, and automatic JSON-to-Python object conversion.
- **Minimal Dependencies**: Lightweight and fast.
- **Advanced Configuration**: Supports `.toml` files for timeout, proxy, and certificate management.

## 📦 Installation

Install the latest version from PyPI:
```bash
pip install pycalendar-api
```

## Quick Start & Usage Examples

Ensure that you are registered, if not, you can [Register](https://calendar-api.ma/console/register) for free 

Instanciate the API Client by providing one the active APIKeys from your console

```python
from pycalendar_api import CalendarApi, to_date  # Util function for date creation

>>> api = CalendarApi('YOUR_API_KEY')
>>> print(api.health())
ApiHealth(api_status="UP", appname="calendar-api", timestamp=datetime.datetime.now())
```

#### Using the environment variable `PYCALENDAR_APIKEY`

```python
# Ensure that the environment variable is defined
# export PYCALENDAR_APIKEY = YOUR_API_KEY
from pycalendar_api import CalendarApi, to_date  # Util function for date creation

>>> api = CalendarApi.from_env()
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

## 🏷️ Enum Properties

Those properties are present in the Response objects and are used as query parameters.

### 🗂️ Holiday Type (`StrEnum`)

A Holiday has one of those types

|       Value       | Description                                                                 |
| :---------------: | --------------------------------------------------------------------------- |
|    **National**   | The date is a national Holiday                                              |
|   **Religious**   | The date is a Religious Holiday (Check the status if it's Confirmed or not) |
|  **Exceptional**  | The date is an exceptional or bridge Holiday                                |

### 🌕 Holiday Status (`StrEnum`)

Those properties concern the religious holidays which are `Estimated` before the moon sighting,
once confirmed their status change to `Official`.

Consider using polling (Every Hour) for religious holidays which are estimated.

|      Value      | Description                                               |
| :-------------: | --------------------------------------------------------- |
|   **Official**  | The Holiday is Official                                   |
|  **Estimated**  | Religious Holidays are estimated before the moon sighting |

## 🛠️ Support

If you encounter any bugs or have questions, we are here to help:

- ✉️ **Email Support**: [support@calendar-api.ma](mailto:support@calendar-api.ma)
- 🐛 **Issue Tracker**: [GitLab Repository Issues](https://gitlab.com/ud-labs/py-calendar-api/-/issues)
- 📝 **Contact Form**: [calendar-api.ma/contacts.html](https://calendar-api.ma/contacts.html)
