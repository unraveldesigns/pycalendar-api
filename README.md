# Calendar API Client

[![Latest Release](https://gitlab.com/ud-labs/py-calendar-api/-/badges/release.svg)](https://gitlab.com/ud-labs/py-calendar-api/-/releases)

A Python 3.12+ client for [Calendar API](https://calendar-api.ma)

Easy and free registration to [Calendar API](https://calendar-api.ma/console/register)

Documentation: [Learn more about the client and Calendar API](https://docs.calendar-api.ma)

##### Features

- Fully typed
- Automatic conversion of Json responses to Python Objects
- **dataclasses** based models (Standard library)
- Modern Http client based on [Niquests](https://niquests.readthedocs.io/en/latest/index.html)
- Advanced `.toml` file configuration
- Minimal dependencies

## Presentation

[Calendar API](https://calendar-api.ma/console/register) covers the holidays and business days domains while providing to Analysts, developers and businesses a centralized service
for needs such as:

- Orchestration and Scheduling of tasks or jobs
- Data analysis: Finding missing dates in a dataset or aligning many datasets
- Data Quality
- Integration with a Date-Picker for UI uses. see tutorial in the product page
- Integration with Airflow by using the advanced configuration of the client pycalendar-api

## Quickstart

Install from Pypi

```bash
pip install pycalendar-api
```

Ensure that you are registered, if not, you can register for free [Here](https://calendar-api.ma/console/register)

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

### Holidays API

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

### Business Days API

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

## Enum properties

Those properties are present in the Response objects and are used as query parameters.

- #### Holiday Type (StrEnum)

A Holiday has one of those types

|       Value       | Description                                                                 |
| :---------------: | --------------------------------------------------------------------------- |
|    **National**   | The date is a national Holiday                                              |
|   **Religious**   | The date is a Religious Holiday (Check the status if it's Confirmed or not) |
|  **Exceptional**  | The date is an exceptional or bridge Holiday                                |

- #### HolidayStatus (StrEnum)

Those properties concern the religious holidays which are `Estimated` before the moon sighting,
once confirmed their status change to `Official`.

Consider using polling (Every Hour) for religious holidays which are estimated.

|      Value      | Description                                               |
| :-------------: | --------------------------------------------------------- |
|   **Official**  | The Holiday is Official                                   |
|  **Estimated**  | Religious Holidays are estimated before the moon sighting |

## Support

If you find any bug or issue please let us know by:

- Mailing us at: [Support](mailto:support@calendar-api.ma)
- Filing an issue in the repository: [Project Repository](https://gitlab.com/ud-labs/py-calendar-api/-/issues)
- Fill the [Contact Form](https://calendar-api.ma/contacts.html)
