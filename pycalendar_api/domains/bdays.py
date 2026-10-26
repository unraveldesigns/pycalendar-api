import datetime

from pycalendar_api.exceptions import CalendarAPIParamError
from pycalendar_api.models import CalSpan, DateSeries, DaysCount, NextDate, PreviousDate
from pycalendar_api.utils import to_int

from .base import ApiCall, AsyncResourceMixin, BaseMixin, SyncResourceMixin
from .urls import ENDPOINTS


class BDaysCalls(BaseMixin):
    """Builds the `ApiCall` of the Business days domain. Shared by the sync and async resources."""

    resource_name = "bdays"
    endpoints = ENDPOINTS

    def _between_call(self, start: datetime.date, end: datetime.date) -> ApiCall:
        pms = {'start': start, 'end': end}
        return ApiCall(self.endpoint_by_operation('between'), params=pms, model_type=DateSeries)

    def _bdays_of_call(self, year: int, month: int=None) -> ApiCall:
        key = 'year'
        pms = {'year': year}
        if month:
            key = 'month'
            pms['month'] = to_int(month)

        url = self.endpoint_by_operation(key).format(**pms)
        return ApiCall(url, model_type=DateSeries)

    def _count_call(self, start: datetime.date, end: datetime.date) -> ApiCall:
        pms = {'start': start, 'end': end}
        return ApiCall(self.endpoint_by_operation('count'), params=pms, model_type=DaysCount)

    def _next_date_call(self, date: datetime.date) -> ApiCall:
        return ApiCall(self.endpoint_by_operation('next'), params={'date': date}, model_type=NextDate)

    def _previous_date_call(self, date: datetime.date) -> ApiCall:
        return ApiCall(self.endpoint_by_operation('previous'), params={'date': date}, model_type=PreviousDate)

    def _span_call(self, year: int, *, month: int=None, quarter: int=None, semester: int=None) -> ApiCall:
        args = (month, quarter, semester)
        t_args = sum([x is None for x in args])
        # Au max un seul argument doit être renseigné.
        # On compte les arguments nuls, Si 2 ou tous renseignés t_args = (0, 1)
        if t_args < 2:
            raise CalendarAPIParamError(f"Pass ONLY one of the args: `month` or `quarter` or `semester`, received: {month=}, {quarter=}, {semester=}")

        key = None
        params = {'year': year}

        if t_args == 3:  # Span Year => All args are None
            key = 'span:year'
        elif month:  # Span Month
            params['month'] = month
            key = 'span:month'
        elif quarter:  # Span quarter
            params['quarter'] = quarter
            key = 'span:quarter'
        elif semester:  # Span semester
            params['semester'] = semester
            key = 'span:semester'

        return ApiCall(self.endpoint_by_operation(key), params=params, model_type=CalSpan)


class BDaysResource(SyncResourceMixin, BDaysCalls):

    def between(self, start: datetime.date, end: datetime.date) -> DateSeries:
        """Get the Business days between 2 dates

        Args:
            start (datetime.date): Start date
            end (datetime.date): End date

        Returns:
            DateSeries: Ordered Set of dates. The collection is under `DateSeries.serie`
        """
        return self._fetch(self._between_call(start, end))

    def bdays_of(self, year: int, month: int=None) -> DateSeries:
        """Get the Business days of a year.

        Args:
            year (int): the year
            month (int, optional): If provided returns the business days of that month

        Returns:
            DateSeries: Ordered Set of dates. The collection is under `DateSeries.serie`
        """
        return self._fetch(self._bdays_of_call(year, month))

    def count(self, start: datetime.date, end: datetime.date) -> DaysCount:
        """Count the business days (inclusive) between 2 dates

        Args:
            start (datetime.date): Start date
            end (datetime.date): End date

        Returns:
            DaysCount: Days count datastruct
        """
        return self._fetch(self._count_call(start, end))

    def next_date(self, date: datetime.date) -> NextDate:
        """Returns the `next` Business day following the provided date

        Args:
            date (datetime.date): A date

        Returns:
            NextDate: Contains the requested date and the next open date
        """
        return self._fetch(self._next_date_call(date))

    def previous_date(self, date: datetime.date) -> PreviousDate:
        """Returns the `previous` Business day before the provided date

        Args:
            date (datetime.date): A date

        Returns:
            PreviousDate: Contains the requested date and the previous open date
        """
        return self._fetch(self._previous_date_call(date))

    # ============ Spans =============
    def span(self, year: int, *, month: int=None, quarter: int=None, semester: int=None) -> CalSpan:
        """Get the Start/End dates of periods (Quarters, Semesters, Months) in the form of ]`Start`, `End`] (Open-Close Interval).

        - `Start`: The last Open Business day of the previous period

        - `End`: The last Open Business day of the period

        Args:
            year (int): Span of a year
            month (int, optional): Span of a month, 1 <= month <= 12
            quarter (int, optional): Span of a quarter, 1 <= quarter <= 4
            semester (int, optional): Span of a semester, 1 <= semester <= 2

        Returns:
            CalSpan: Span interval of the requested period

        Raises:
            CalendarAPIParamError: Only one of the periods must be provided.
        """
        return self._fetch(self._span_call(year, month=month, quarter=quarter, semester=semester))


class AsyncBDaysResource(AsyncResourceMixin, BDaysCalls):
    """Async version of `BDaysResource`. Same operations, to be awaited."""

    async def between(self, start: datetime.date, end: datetime.date) -> DateSeries:
        """Get the Business days between 2 dates. See `BDaysResource.between`"""
        return await self._fetch(self._between_call(start, end))

    async def bdays_of(self, year: int, month: int=None) -> DateSeries:
        """Get the Business days of a year or a month. See `BDaysResource.bdays_of`"""
        return await self._fetch(self._bdays_of_call(year, month))

    async def count(self, start: datetime.date, end: datetime.date) -> DaysCount:
        """Count the business days (inclusive) between 2 dates. See `BDaysResource.count`"""
        return await self._fetch(self._count_call(start, end))

    async def next_date(self, date: datetime.date) -> NextDate:
        """Returns the `next` Business day following the provided date. See `BDaysResource.next_date`"""
        return await self._fetch(self._next_date_call(date))

    async def previous_date(self, date: datetime.date) -> PreviousDate:
        """Returns the `previous` Business day before the provided date. See `BDaysResource.previous_date`"""
        return await self._fetch(self._previous_date_call(date))

    # ============ Spans =============
    async def span(self, year: int, *, month: int=None, quarter: int=None, semester: int=None) -> CalSpan:
        """Get the Start/End dates of periods. See `BDaysResource.span`

        Raises:
            CalendarAPIParamError: Only one of the periods must be provided.
        """
        return await self._fetch(self._span_call(year, month=month, quarter=quarter, semester=semester))
