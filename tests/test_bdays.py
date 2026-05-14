import pytest

from pycalendar_api import CalendarApi
from pycalendar_api.utils import to_date

pytestmark = pytest.mark.client


BDAYS_COUNT_2025 = 247

# ---- Business Days ----
def test_bdays_next_day(api_client: CalendarApi):
    adate = to_date('17/11/2025')
    cible = to_date('19/11/2025')
    res = api_client.bdays.next_date(adate)
    assert res.next_date == cible


def test_bdays_previous_day(api_client: CalendarApi):
    adate = to_date('19/11/2025')
    cible = to_date('17/11/2025')
    res = api_client.bdays.previous_date(adate)
    assert res.previous_date == cible


def test_bdays_spans(api_client: CalendarApi):
    year = 2025
    semester = 1
    quarter = 3
    month = 7
    span_year = api_client.bdays.span(year)
    assert span_year.year == year

    span_semester = api_client.bdays.span(year, semester=semester)
    assert span_semester.year == year
    assert span_semester.semester == semester

    span_quarter = api_client.bdays.span(year, quarter=quarter)
    assert span_quarter.year == year
    assert span_quarter.quarter == quarter

    span_month = api_client.bdays.span(year, month=month)
    assert span_month.year == year
    assert span_month.month == month


def test_bdays_count(api_client: CalendarApi):
    start = to_date('01/01/2025')
    end = to_date('31/12/2025')
    count = api_client.bdays.count(start, end)
    assert count.start_date == to_date('02/01/2025'), "La date de début doit inclure le premier jour ouvrable qui est le 02/01/2025"
    assert count.count == BDAYS_COUNT_2025


def test_bdays_serie(api_client: CalendarApi):
    year = 2025
    date_serie = api_client.bdays.bdays_of(year)
    assert date_serie.min_date == to_date('02/01/2025'), "La date de début doit inclure le premier jour ouvrable qui est le 02/01/2025"
    assert date_serie.nitems == len(date_serie.serie)
    assert date_serie.nitems == BDAYS_COUNT_2025
