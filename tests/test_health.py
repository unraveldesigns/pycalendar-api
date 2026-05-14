import pytest

from pycalendar_api import CalendarApi
from pycalendar_api.models import ApiHealth

pytestmark = pytest.mark.client

# ---- Health endpoint ----

def test_health_endpoint(api_client: CalendarApi):
    res = api_client.health()
    assert isinstance(res, ApiHealth)
    assert res.appname == 'calendar-api'
    assert res.api_status == 'UP'
