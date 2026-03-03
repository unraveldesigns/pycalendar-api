# Calendar API Client

A python 3.12+ client for the calendar-api API of Moroccan holidays and business days

## Installation

```bash
pip install pycalendar-api --index-url https://gitlab.com/api/v4/projects/79644191/packages/pypi/simple
```

## Quickstart

### Holidays API

```python
from pycalendar_api import CalendarApi, to_date

api = CalendarApi('YOUR_API_KEY') # or api = CalendarApi.from_env()

# Check if a date is a Holiday
api.holidays.is_holiday(to_date('14/01/2025'))
Out[]: HolidayCheckResult(
    date=datetime.date(2025, 7, 22), is_holiday=False,
    description=None, holiday_type=None, status=None, country_code='MA'
)

# List Holidays of a year
api.holidays.year(2025)
Out[]: [
    Holiday(description="Jour de l'AN", day=1, month=1, date=datetime.date(2025, 1, 1), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    Holiday(description="Manifeste de l'Indépendance", day=11, month=1, date=datetime.date(2025, 1, 11), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    Holiday(description='Nouvel An Amazigh', day=14, month=1, date=datetime.date(2025, 1, 14), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    ...,
]

# List Holidays of many years
api.holidays.years(list(range(2017, 2027)))
Out[]: [
    Holiday(description="Jour de l'AN", day=1, month=1, date=datetime.date(2025, 1, 1), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    Holiday(description="Manifeste de l'Indépendance", day=11, month=1, date=datetime.date(2025, 1, 11), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    Holiday(description='Nouvel An Amazigh', day=14, month=1, date=datetime.date(2025, 1, 14), holiday_type=<CalHolidayType.NATIONAL: 'National'>, status=<CalHolidayStatus.OFFICIAL: 'Official'>, country_code='MA'),
    ...,
]
```

### Business Days API

#### Bdays operations

```python
# Business days of a year
api.bdays.bdays_of(2025)
Out[]: DateSeries(
   ref='bdays-2025', min_date='2025-01-02', max_date='2025-12-31', freq=<CalFreq.DAILY: 'D'>, nitems=247,
   serie=SortedSet([datetime.date(2025, 1, 2), datetime.date(2025, 1, 3), datetime.date(2025, 1, 6), ..., datetime.date(2025, 12, 29), datetime.date(2025, 12, 30), datetime.date(2025, 12, 31)])
)

# Business days of a month
api.bdays.bdays_of(2025, month=6)
Out[]: DateSeries(
   ref='bdays-2025-06', min_date='2025-06-02', max_date='2025-06-30', freq=<CalFreq.DAILY: 'D'>, nitems=19,
   serie=SortedSet([datetime.date(2025, 6, 2), datetime.date(2025, 6, 3), datetime.date(2025, 6, 4), datetime.date(2025, 6, 5), ..., datetime.date(2025, 6, 25), datetime.date(2025, 6, 26), datetime.date(2025, 6, 30)])
)

# Next Business day
api.bdays.next_date(to_date('13/01/2025'))
Out[]: NextDate(date=datetime.date(2025, 1, 13), next_date=datetime.date(2025, 1, 15))

# Previous Business day
api.bdays.previous_date(to_date('15/01/2025'))
Out[]: NextDate(date=datetime.date(2025, 1, 15), previous_date=datetime.date(2025, 1, 13))

# Business days between 2 dates
api.bdays.count(to_date('02/01/2025'), to_date('31/12/2025'))
Out[25]: DaysCount(start_date=datetime.date(2025, 1, 2), end_date=datetime.date(2025, 12, 31), count=247, freq=<CalFreq.DAILY: 'D'>)
```

#### Spans: Start/End of periods

Calculate the dates interval of different periods

```python
# =============== SPANS: Start/End of periods ===============
# Year 2025 span
api.bdays.span(2025)
Out[]: CalSpan(start_date=datetime.date(2024, 12, 31), end_date=datetime.date(2025, 12, 31), year=2025, semester=None, quarter=None, month=None, country_code='MA')

# 1st Semester of year 2025
api.bdays.span(2025, semester=1)
Out[]: CalSpan(start_date=datetime.date(2024, 12, 31), end_date=datetime.date(2025, 6, 30), year=2025, semester=1, quarter=None, month=None, country_code='MA')

# 3rd Quarter of year 2025
api.bdays.span(2025, quarter=3)
Out[]: CalSpan(start_date=datetime.date(2025, 6, 30), end_date=datetime.date(2025, 9, 30), year=2025, semester=None, quarter=3, month=None, country_code='MA')

# Month 7 of year 2025 (July) 
api.bdays.span(2025, month=7)
Out[]: CalSpan(start_date=datetime.date(2025, 6, 30), end_date=datetime.date(2025, 7, 31), year=2025, semester=None, quarter=None, month=7, country_code='MA')
```
