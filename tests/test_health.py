import pytest

from pycalendar_api import AsyncCalendarApi, CalendarApi
from pycalendar_api.models import ApiHealth

pytestmark = [pytest.mark.client, pytest.mark.live]

# ---- Health endpoint ----

def test_health_endpoint(api_client: CalendarApi):
    res = api_client.health()
    assert isinstance(res, ApiHealth)
    assert res.appname == 'calendar-api'
    assert res.api_status == 'UP'


@pytest.mark.anyio
async def test_health_endpoint_async(async_api_client: AsyncCalendarApi):
    res = await async_api_client.health()
    assert isinstance(res, ApiHealth)
    assert res.api_status == 'UP'
