import datetime

import httpxyz

from pycalendar_api.exceptions import CalendarAPIParamError
from pycalendar_api.models import CalSpan, DateSeries, DaysCount, NextDate, PreviousDate
from pycalendar_api.utils import to_int

from .base import BaseMixin
from .urls import ENDPOINTS


class BDaysResource(BaseMixin):

    resource_name = "bdays"

    def __init__(self, client: httpxyz.Client):
        super().__init__(client, endpoints=ENDPOINTS)

    def between(self, start: datetime.date, end: datetime.date) -> DateSeries:
        """Get the Business days between 2 dates

        Args:
            start (datetime.date): Start date
            end (datetime.date): End date

        Returns:
            DateSeries: Ordered Set of dates. The collection is under `DateSeries.serie`
        """
        key = 'between'
        pms = {'start': start, 'end': end}
        url = self.endpoint_by_operation(key)
        resp = self.client.get(url, params=pms)
        data = self.json_from_response_or_raise(resp)
        return self._struct_model(data, model_type=DateSeries)

    def bdays_of(self, year: int, month: int=None) -> DateSeries:
        """Get the Business days of a year.

        Args:
            year (int): the year
            month (int, optional): If provided returns the business days of that month

        Returns:
            DateSeries: Ordered Set of dates. The collection is under `DateSeries.serie`
        """
        key = 'year'
        pms = {'year': year}
        if month:
            key = 'month'
            pms['month'] = to_int(month)

        url = self.endpoint_by_operation(key)
        url = url.format(**pms)
        resp = self.client.get(url)
        data = self.json_from_response_or_raise(resp)
        return self._struct_model(data, model_type=DateSeries)

    def count(self, start: datetime.date, end: datetime.date) -> DaysCount:
        """Count the business days (inclusive) between 2 dates

        Args:
            start (datetime.date): Start date
            end (datetime.date): End date

        Returns:
            DaysCount: Days count datastruct
        """
        key = 'count'
        pms = {'start': start, 'end': end}
        url = self.endpoint_by_operation(key)
        resp = self.client.get(url, params=pms)
        data = self.json_from_response_or_raise(resp)
        return self._struct_model(data, model_type=DaysCount)

    def next_date(self, date: datetime.date) -> NextDate:
        """Returns the `next` Business day following the provided date

        Args:
            date (datetime.date): A date

        Returns:
            NextDate: Contains the requested date and the next open date
        """
        url = self.endpoint_by_operation('next')
        params = {'date': date}
        data = self.json_from_response_or_raise(self.client.get(url, params=params))
        return self._struct_model(data, model_type=NextDate)

    def previous_date(self, date: datetime.date) -> PreviousDate:
        """Returns the `previous` Business day before the provided date

        Args:
            date (datetime.date): A date

        Returns:
            PreviousDate: Contains the requested date and the previous open date
        """
        url = self.endpoint_by_operation('previous')
        params = {'date': date}
        data = self.json_from_response_or_raise(self.client.get(url, params=params))
        return self._struct_model(data, model_type=PreviousDate)

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

        url = self.endpoint_by_operation(key)
        resp = self.client.get(url, params=params)
        data = self.json_from_response_or_raise(resp)
        return self._struct_model(data, model_type=CalSpan)
