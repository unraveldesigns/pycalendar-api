import datetime

import pytest

from pycalendar_api import AsyncCalendarApi, CalendarApi
from pycalendar_api.properties import DayKind

pytestmark = [pytest.mark.client, pytest.mark.live]


# ---- Tagged Calendar ----
def test_tagged_month(api_client: CalendarApi):
    res = api_client.tagged.month(2026, 1)
    assert (res.year, res.month) == (2026, 1)
    assert [d.date for d in res] == [datetime.date(2026, 1, d) for d in range(1, 32)]
    assert res.counts.total == 31
    amazigh = res.days[13]
    assert amazigh.is_holiday is True, "Erreur de configuration au niveau du serveur. Call support@calendar-api.ma"
    assert amazigh.day_kind == DayKind.HOLIDAY


def test_tagged_year(api_client: CalendarApi):
    res = api_client.tagged.year(2026)
    assert [m.month for m in res.months] == list(range(1, 13))
    assert res.counts.total == len(res.days) == 365


@pytest.mark.anyio
async def test_async_tagged_month(async_api_client: AsyncCalendarApi):
    res = await async_api_client.tagged.month(2026, 1)
    assert res.counts.total == 31
