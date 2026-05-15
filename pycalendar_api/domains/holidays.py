import datetime
from collections.abc import Iterable

import niquests

from pycalendar_api.models import Holiday, HolidayCheckResult
from pycalendar_api.properties import CalHolidayType

from .base import BaseMixin
from .urls import ENDPOINTS


class HolidaysResource(BaseMixin):

    resource_name = "holidays"

    def __init__(self, client: niquests.Session):
        super().__init__(client, endpoints=ENDPOINTS)

    def year(self, year: int, *, holiday_type: CalHolidayType=None) -> list[Holiday]:
        """Get the holidays of a year

        Args:
            year (int): the Year
            holiday_type (`CalHolidayType`): Optional filter on holiday type. See `CalHolidayType`

        Returns:
            list[Holiday]: Ordered list of holidays of one year
        """
        key = 'year'
        qp = {}
        pms = {'year': year}
        if holiday_type:
            qp = {'holiday_type': holiday_type}

        endpoint = self.endpoint_by_operation(key)
        url = endpoint.format(**pms)
        resp = self.client.get(url, params=qp)
        data = self.json_from_response_or_raise(resp)
        rv = [self._struct_model(d, model_type=Holiday) for d in data]
        return rv

    def years(self, years: Iterable[int], *, holiday_type: CalHolidayType=None) -> list[Holiday]:
        """Get the holidays of many years

        Args:
            year (Iterable[int]): Iterable of years as int
            holiday_type (`CalHolidayType`): Optional filter on holiday type. See `CalHolidayType`

        Returns:
            list[Holiday]: Ordered list of holidays spanning many years
        """
        key = 'years'
        years = years if isinstance(years, Iterable) else [years]
        pms = {'years': years}
        if holiday_type:
            pms['holiday_type'] = holiday_type

        url = self.endpoint_by_operation(key)
        resp = self.client.get(url, params=pms)
        data = self.json_from_response_or_raise(resp)
        rv = [self._struct_model(d, model_type=Holiday) for d in data]
        return rv

    def is_holiday(self, date: datetime.date) -> HolidayCheckResult:
        """Verify if the provided date is a Holiday. If True, also returns the description of that Holiday and its type.

        Args:
            date (datetime.date): A date

        Returns:
            HolidayCheckResult: Result of the verification
        """
        key = 'is-holiday'
        pms = {'date': date}
        url = self.endpoint_by_operation(key)
        resp = self.client.get(url, params=pms)
        data = self.json_from_response_or_raise(resp)
        return self._struct_model(data, model_type=HolidayCheckResult)
