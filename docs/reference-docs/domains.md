# Endpoints adapters (Domains)

Endpoints are grouped under tags which represent a domain exposed by the API.

Calendar API exposes 3 domains:

- Holidays: Holidays related operations
- Bdays: Business Days related operations
- Tagged Calendar: Both of them merged, every day tagged with its kind. This is the whole calendar

In the client side, the domains are represented as Resource adapters

::: pycalendar_api.domains.base.BaseMixin
    :docstring:

::: pycalendar_api.domains.holidays.HolidaysResource
    :docstring:

::: pycalendar_api.domains.bdays.BDaysResource
    :docstring:

::: pycalendar_api.domains.tagged.TaggedCalendarResource
    :docstring:

::: pycalendar_api.domains.health.HealthsResource
    :docstring:

## Async resources

`AsyncCalendarApi` uses the async counterparts of the resources above. They share the same requests (`ApiCall`) and the same models.

::: pycalendar_api.domains.base.ApiCall
    :docstring:

::: pycalendar_api.domains.holidays.AsyncHolidaysResource
    :docstring:

::: pycalendar_api.domains.bdays.AsyncBDaysResource
    :docstring:

::: pycalendar_api.domains.tagged.AsyncTaggedCalendarResource
    :docstring:

::: pycalendar_api.domains.health.AsyncHealthsResource
    :docstring:
