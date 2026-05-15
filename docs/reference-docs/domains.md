# Endpoints adapters (Domains)

Endpoints are grouped under tags which represent a domain exposed by the API.

Calendar API exposes 2 domains:

- Holidays: Holidays related operations
- Bdays: Business Days related operations

Conceptually if we merge the results of both of them we will have the whole calendar

In the client side, the domains are represented as Resource adapters

::: pycalendar_api.domains.base.BaseMixin
    :docstring:

::: pycalendar_api.domains.holidays.HolidaysResource
    :docstring:

::: pycalendar_api.domains.bdays.BDaysResource
    :docstring:
