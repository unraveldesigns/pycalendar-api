"""Offline tests of the domains, run against both `CalendarApi` and `AsyncCalendarApi`.

The real clients (headers, hooks, base url) are used, only the transport is mocked. See `conftest.FakeServer`.
"""
import inspect
from datetime import date

import httpx
import pytest

from pycalendar_api import AsyncCalendarApi, CalendarApi, CalendarAPIAuthError, CalendarAPIParamError
from pycalendar_api.models import (
    CalSpan,
    DateSeries,
    DaysCount,
    Holiday,
    HolidayCheckResult,
    NextDate,
    PreviousDate,
    TaggedDay,
    TaggedMonth,
    TaggedYear,
)
from pycalendar_api.properties import CalFreq, CalHolidayStatus, CalHolidayType, DayKind

from .conftest import FAKE_APIKEY, FakeServer

pytestmark = [pytest.mark.client, pytest.mark.anyio]

API = "/api/v1"

HOLIDAY = {
    'description': 'Nouvel an amazigh', 'day': 14, 'month': 1, 'date': '2026-01-14',
    'holiday_type': 'National', 'status': 'Official', 'country_code': 'MA',
}


@pytest.fixture(name='api', params=['sync', 'async'])
async def fx_api(request: pytest.FixtureRequest, fake_server: FakeServer):
    transport = httpx.MockTransport(fake_server)
    if request.param == 'sync':
        with CalendarApi(FAKE_APIKEY, transport=transport) as api:
            yield api
    else:
        async with AsyncCalendarApi(FAKE_APIKEY, transport=transport) as api:
            yield api


async def resolve(value):
    """Await the result of the async client, pass through the result of the sync one"""
    return await value if inspect.isawaitable(value) else value


# ---- Client ----
async def test_client_headers(api, fake_server: FakeServer):
    fake_server.route('/health', {'api_status': 'UP', 'appname': 'calendar-api'})
    await resolve(api.health())
    headers = fake_server.last.headers
    assert headers['X-API-KEY'] == FAKE_APIKEY
    assert headers['X-CLIENT'] == 'pycalendar-api'
    assert 'X-CLIENT-VERSION' in headers
    assert 'x-timestamp' in headers, "The request event hook must run on both clients"


async def test_health_is_served_at_the_host_root(api, fake_server: FakeServer):
    fake_server.route('/health', {'api_status': 'UP', 'appname': 'calendar-api'})
    res = await resolve(api.health())
    assert str(fake_server.last.url) == 'https://calendar-api.ma/health'
    assert res.api_status == 'UP'


async def test_auth_error(api, fake_server: FakeServer):
    fake_server.route(f'{API}/bdays/next', {'status_code': 401, 'detail': 'Invalid X-API-KEY header!'}, status_code=401)
    with pytest.raises(CalendarAPIAuthError, match='Invalid X-API-KEY'):
        await resolve(api.bdays.next_date(date(2025, 11, 17)))


# ---- Business Days ----
async def test_bdays_between(api, fake_server: FakeServer):
    fake_server.route(f'{API}/bdays/between', {'ref': 'between', 'freq': 'D', 'serie': ['2025-01-03', '2025-01-02']})
    res = await resolve(api.bdays.between(date(2025, 1, 1), date(2025, 1, 3)))
    assert fake_server.last.url.params == httpx.QueryParams({'start': '2025-01-01', 'end': '2025-01-03'})
    assert isinstance(res, DateSeries)
    assert list(res) == [date(2025, 1, 2), date(2025, 1, 3)]
    assert res.min_date == date(2025, 1, 2)
    assert res.freq == CalFreq.DAILY


@pytest.mark.parametrize(("month", "path"), [(None, '/bdays/2025'), (7, '/bdays/2025/7'), ('07', '/bdays/2025/7')])
async def test_bdays_of(api, fake_server: FakeServer, month, path: str):
    fake_server.route(f'{API}{path}', {'ref': '2025', 'serie': ['2025-07-01']})
    res = await resolve(api.bdays.bdays_of(2025, month))
    assert fake_server.last.url.path == f'{API}{path}'
    assert res.nitems == 1


async def test_bdays_count(api, fake_server: FakeServer):
    fake_server.route(f'{API}/bdays/count', {'start_date': '2025-01-02', 'end_date': '2025-12-31', 'count': 247, 'freq': 'D'})
    res = await resolve(api.bdays.count(date(2025, 1, 1), date(2025, 12, 31)))
    assert isinstance(res, DaysCount)
    assert res.count == 247
    assert res.start_date == date(2025, 1, 2)


async def test_bdays_next_previous(api, fake_server: FakeServer):
    fake_server.route(f'{API}/bdays/next', {'date': '2025-11-17', 'next_date': '2025-11-19'})
    fake_server.route(f'{API}/bdays/previous', {'date': '2025-11-19', 'previous_date': '2025-11-17'})

    nxt = await resolve(api.bdays.next_date(date(2025, 11, 17)))
    assert fake_server.last.url.params['date'] == '2025-11-17'
    assert nxt == NextDate(date(2025, 11, 17), date(2025, 11, 19))

    prev = await resolve(api.bdays.previous_date(date(2025, 11, 19)))
    assert prev == PreviousDate(date(2025, 11, 19), date(2025, 11, 17))


@pytest.mark.parametrize(
    ("kwargs", "path", "params"),
    [
        ({}, '/bdays/span/year', {'year': '2025'}),
        ({'month': 7}, '/bdays/span/month', {'year': '2025', 'month': '7'}),
        ({'quarter': 3}, '/bdays/span/quarter', {'year': '2025', 'quarter': '3'}),
        ({'semester': 1}, '/bdays/span/semester', {'year': '2025', 'semester': '1'}),
    ],
)
async def test_bdays_span(api, fake_server: FakeServer, kwargs: dict, path: str, params: dict):
    fake_server.route(f'{API}{path}', {'year': 2025, **kwargs, 'start_date': '2024-12-31', 'end_date': '2025-12-31'})
    res = await resolve(api.bdays.span(2025, **kwargs))
    assert fake_server.last.url.path == f'{API}{path}'
    assert fake_server.last.url.params == httpx.QueryParams(params)
    assert isinstance(res, CalSpan)
    assert res.end_date == date(2025, 12, 31)


@pytest.mark.parametrize("kwargs", [{'month': 1, 'quarter': 1}, {'month': 1, 'semester': 1}, {'month': 1, 'quarter': 1, 'semester': 1}])
async def test_bdays_span_rejects_many_periods(api, fake_server: FakeServer, kwargs: dict):
    with pytest.raises(CalendarAPIParamError):
        await resolve(api.bdays.span(2025, **kwargs))
    assert not fake_server.requests, "Invalid params must be rejected before any request"


# ---- Holidays ----
async def test_holidays_year(api, fake_server: FakeServer):
    fake_server.route(f'{API}/holidays/2026', [HOLIDAY])
    res = await resolve(api.holidays.year(2026))
    assert not fake_server.last.url.params
    assert res == [Holiday(**HOLIDAY)]
    assert res[0].holiday_type == CalHolidayType.NATIONAL

    await resolve(api.holidays.year(2026, holiday_type=CalHolidayType.RELIGIOUS))
    assert fake_server.last.url.params['holiday_type'] == 'Religious'


@pytest.mark.parametrize(("years", "expected"), [((2026, 2027), ['2026', '2027']), ([2026], ['2026']), (2026, ['2026']), ('2026', ['2026'])])
async def test_holidays_years(api, fake_server: FakeServer, years, expected: list[str]):
    fake_server.route(f'{API}/holidays/years', [HOLIDAY, HOLIDAY])
    res = await resolve(api.holidays.years(years, holiday_type=CalHolidayType.NATIONAL))
    assert fake_server.last.url.params.get_list('years') == expected
    assert fake_server.last.url.params['holiday_type'] == 'National'
    assert len(res) == 2


async def test_holidays_is_holiday(api, fake_server: FakeServer):
    payload = {k: v for k, v in HOLIDAY.items() if k not in ('day', 'month')} | {'is_holiday': True}
    fake_server.route(f'{API}/holidays/is-holiday', payload)
    res = await resolve(api.holidays.is_holiday(date(2026, 1, 14)))
    assert fake_server.last.url.params['date'] == '2026-01-14'
    assert isinstance(res, HolidayCheckResult)
    assert res.is_holiday is True
    assert res.status == CalHolidayStatus.OFFICIAL


# ---- Tagged Calendar ----
def tagged_day(day: date) -> dict | None:
    """`TaggedDayEng` payload of the server for January 2026: the 1st and the 14th are holidays"""
    holidays = {1: 'Nouvel an', 14: 'Nouvel an amazigh'}
    is_weekend = day.weekday() >= 5
    is_holiday = day.day in holidays
    kind = 'WEEKEND' if is_weekend else 'HOLIDAY' if is_holiday else 'BUSINESS'
    return {
        'date': day.isoformat(), 'day_kind': kind,
        'is_business_day': kind == 'BUSINESS', 'is_weekend': is_weekend, 'is_holiday': is_holiday,
        'holiday_type': 'National' if is_holiday else None,
        'status': 'Official' if is_holiday else None,
        'description': holidays.get(day.day),
        'label': f"Jan {day.day} — {holidays.get(day.day, 'Weekend' if is_weekend else 'Business day')}",
        'country_code': 'MA',
    }


def tagged_january() -> dict:
    """`TaggedMonthEng` payload: 2026-01-01 is a Thursday, the weeks are padded with `null`"""
    days = [None] * 3 + [tagged_day(date(2026, 1, d)) for d in range(1, 32)] + [None]
    return {
        'year': 2026, 'month': 1, 'label': 'January 2026',
        'weekday_labels': ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'],
        'counts': {'business_days': 20, 'weekend_days': 9, 'holidays': 2},
        'weeks': [days[i:i + 7] for i in range(0, len(days), 7)],
    }


@pytest.mark.parametrize("month", [1, '01'])
async def test_tagged_month(api, fake_server: FakeServer, month):
    fake_server.route(f'{API}/tagged-calendar/2026/1', tagged_january())
    res = await resolve(api.tagged.month(2026, month))
    assert fake_server.last.url.path == f'{API}/tagged-calendar/2026/1'
    assert isinstance(res, TaggedMonth)
    assert res.label == 'January 2026'
    assert res.counts.total == 31
    assert len(res.weeks) == 5
    assert all(len(week) == 7 for week in res.weeks)
    assert res.weeks[0][:3] == [None, None, None], "Days outside the month are None"

    assert [d.date for d in res] == [date(2026, 1, d) for d in range(1, 32)]
    first, amazigh, saturday = res.days[0], res.days[13], res.days[2]
    assert isinstance(first, TaggedDay)
    assert (first.day_kind, first.holiday_type, first.status) == (DayKind.HOLIDAY, CalHolidayType.NATIONAL, CalHolidayStatus.OFFICIAL)
    assert amazigh.description == 'Nouvel an amazigh'
    assert saturday.day_kind == DayKind.WEEKEND
    assert saturday.holiday_type is None
    assert sum(d.day_kind == DayKind.BUSINESS for d in res) == res.counts.business_days


async def test_tagged_year(api, fake_server: FakeServer):
    january = tagged_january()
    fake_server.route(f'{API}/tagged-calendar/2026', {'year': 2026, 'counts': january['counts'], 'months': [january]})
    res = await resolve(api.tagged.year(2026))
    assert fake_server.last.url.path == f'{API}/tagged-calendar/2026'
    assert isinstance(res, TaggedYear)
    assert res.counts.holidays == 2
    assert isinstance(res.month(1), TaggedMonth)
    assert len(res.days) == len(list(res)) == 31
    with pytest.raises(KeyError):
        res.month(2)


# ---- OpenAPI schema ----
async def test_openapi_schema(api, fake_server: FakeServer, tmp_path):
    fake_server.route('/schema/openapi.json', {'openapi': '3.1.0', 'paths': {}})
    fpath = await resolve(api.openapi_schema(tmp_path / 'openapi.json'))
    assert str(fake_server.last.url) == 'https://calendar-api.ma/schema/openapi.json'
    assert fpath.read_text().startswith('{"openapi"')
