import pytest

from pycalendar_api import CalendarApi
from pycalendar_api.properties import CalHolidayStatus, CalHolidayType
from pycalendar_api.utils import to_date

pytestmark = pytest.mark.client

# ---- Holidays ----
def test_holidays_is_holiday(api_client: CalendarApi):
    adate = to_date('14/01/2026')
    res = api_client.holidays.is_holiday(adate)
    assert res.date == adate
    assert res.is_holiday is True, "Erreur de configuration au niveau du serveur. Call support@calendar-api.ma"
    assert res.holiday_type == CalHolidayType.NATIONAL
    assert res.status == CalHolidayStatus.OFFICIAL
    assert res.country_code == "MA"


def test_holidays_isnot_holiday(api_client: CalendarApi):
    adate = to_date('15/01/2026')
    res = api_client.holidays.is_holiday(adate)
    assert res.date == adate
    assert res.is_holiday is False
    # assert res.holiday_type == CalHolidayType.NATIONAL
    # assert res.status == CalHolidayStatus.OFFICIAL
    assert res.country_code == "MA"


def test_holidays_year(api_client: CalendarApi):
    year = 2026
    res = api_client.holidays.year(year)
    assert isinstance(res, list)


def test_holidays_years(api_client: CalendarApi):
    years = 2026, 2027
    res = api_client.holidays.years(years)
    assert isinstance(res, list)
