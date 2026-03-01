import datetime

import httpx

from pycalendar_api.exceptions import CalendarAPIParamError
from pycalendar_api.models import Holiday, HolidayCheckResult
from pycalendar_api.properties import CalHolidayType

from .base import BaseMixin
from .urls import ENDPOINTS


class HolidaysResource(BaseMixin):

    resource_name = "holidays"

    def __init__(self, client: httpx.Client):
        super().__init__(client, endpoints=ENDPOINTS)

    def year(self, year: int, *, holiday_type: CalHolidayType=None) -> list[Holiday]:
        key = 'year'
        qp = {}
        pms = {'year': year}
        if holiday_type:
            qp = {'holiday_type': holiday_type}

        endpoint = self.endpoint_by_operation(key)
        url = endpoint.format(**pms)
        resp = self.client.get(url, params=qp)
        data = self.json_from_response_or_raise(resp)
        rv = [Holiday.from_json(d) for d in data]
        return rv

    def years(self, years: list[int], *, holiday_type: CalHolidayType=None) -> list[Holiday]:
        key = 'years'
        pms = {'years': years}
        if holiday_type:
            pms['holiday_type'] = holiday_type

        url = self.endpoint_by_operation(key)
        resp = self.client.get(url, params=pms)
        data = self.json_from_response_or_raise(resp)
        rv = [Holiday.from_json(d) for d in data]
        return rv

    def is_holiday(self, date: datetime.date) -> HolidayCheckResult:
        key = 'is-holiday'
        pms = {'date': date}
        url = self.endpoint_by_operation(key)
        resp = self.client.get(url, params=pms)
        data = self.json_from_response_or_raise(resp)
        return self._struct_model(data, model_type=HolidayCheckResult)
