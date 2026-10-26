import datetime
from collections.abc import Iterable

from pycalendar_api.models import Holiday, HolidayCheckResult
from pycalendar_api.properties import CalHolidayType

from .base import ApiCall, AsyncResourceMixin, BaseMixin, SyncResourceMixin
from .urls import ENDPOINTS


class HolidaysCalls(BaseMixin):
    """Builds the `ApiCall` of the Holidays domain. Shared by the sync and async resources."""

    resource_name = "holidays"
    endpoints = ENDPOINTS

    def _year_call(self, year: int, *, holiday_type: CalHolidayType=None) -> ApiCall:
        qp = {}
        pms = {'year': year}
        if holiday_type:
            qp = {'holiday_type': holiday_type}

        url = self.endpoint_by_operation('year').format(**pms)
        return ApiCall(url, params=qp, model_type=Holiday, many=True)

    def _years_call(self, years: Iterable[int], *, holiday_type: CalHolidayType=None) -> ApiCall:
        years = list(years) if isinstance(years, Iterable) and not isinstance(years, str) else [years]
        pms = {'years': years}
        if holiday_type:
            pms['holiday_type'] = holiday_type

        return ApiCall(self.endpoint_by_operation('years'), params=pms, model_type=Holiday, many=True)

    def _is_holiday_call(self, date: datetime.date) -> ApiCall:
        pms = {'date': date}
        return ApiCall(self.endpoint_by_operation('is-holiday'), params=pms, model_type=HolidayCheckResult)


class HolidaysResource(SyncResourceMixin, HolidaysCalls):

    def year(self, year: int, *, holiday_type: CalHolidayType=None) -> list[Holiday]:
        """Get the holidays of a year

        Args:
            year (int): the Year
            holiday_type (`CalHolidayType`): Optional filter on holiday type. See `CalHolidayType`

        Returns:
            list[Holiday]: Ordered list of holidays of one year
        """
        return self._fetch(self._year_call(year, holiday_type=holiday_type))

    def years(self, years: Iterable[int], *, holiday_type: CalHolidayType=None) -> list[Holiday]:
        """Get the holidays of many years

        Args:
            years (Iterable[int]): Iterable of years as int
            holiday_type (`CalHolidayType`): Optional filter on holiday type. See `CalHolidayType`

        Returns:
            list[Holiday]: Ordered list of holidays spanning many years
        """
        return self._fetch(self._years_call(years, holiday_type=holiday_type))

    def is_holiday(self, date: datetime.date) -> HolidayCheckResult:
        """Verify if the provided date is a Holiday. If True, also returns the description of that Holiday and its type.

        Args:
            date (datetime.date): A date

        Returns:
            HolidayCheckResult: Result of the verification
        """
        return self._fetch(self._is_holiday_call(date))


class AsyncHolidaysResource(AsyncResourceMixin, HolidaysCalls):
    """Async version of `HolidaysResource`. Same operations, to be awaited."""

    async def year(self, year: int, *, holiday_type: CalHolidayType=None) -> list[Holiday]:
        """Get the holidays of a year. See `HolidaysResource.year`"""
        return await self._fetch(self._year_call(year, holiday_type=holiday_type))

    async def years(self, years: Iterable[int], *, holiday_type: CalHolidayType=None) -> list[Holiday]:
        """Get the holidays of many years. See `HolidaysResource.years`"""
        return await self._fetch(self._years_call(years, holiday_type=holiday_type))

    async def is_holiday(self, date: datetime.date) -> HolidayCheckResult:
        """Verify if the provided date is a Holiday. See `HolidaysResource.is_holiday`"""
        return await self._fetch(self._is_holiday_call(date))
