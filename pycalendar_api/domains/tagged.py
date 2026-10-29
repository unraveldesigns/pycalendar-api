from pycalendar_api.models import TaggedMonth, TaggedYear
from pycalendar_api.utils import to_int

from .base import ApiCall, AsyncResourceMixin, BaseMixin, SyncResourceMixin
from .urls import ENDPOINTS


class TaggedCalendarCalls(BaseMixin):
    """Builds the `ApiCall` of the Tagged Calendar domain. Shared by the sync and async resources."""

    resource_name = "tagged"
    endpoints = ENDPOINTS

    def _year_call(self, year: int) -> ApiCall:
        url = self.endpoint_by_operation('year').format(year=to_int(year))
        return ApiCall(url, model_type=TaggedYear)

    def _month_call(self, year: int, month: int) -> ApiCall:
        url = self.endpoint_by_operation('month').format(year=to_int(year), month=to_int(month))
        return ApiCall(url, model_type=TaggedMonth)


class TaggedCalendarResource(SyncResourceMixin, TaggedCalendarCalls):

    def year(self, year: int) -> TaggedYear:
        """Get the full calendar of a year, month by month, where every day is tagged
        `BUSINESS`, `WEEKEND` or `HOLIDAY` (with its type, status and description).

        Args:
            year (int): the Year (2000 → 2040)

        Returns:
            TaggedYear: The months of the year and the days counts by kind
        """
        return self._fetch(self._year_call(year))

    def month(self, year: int, month: int) -> TaggedMonth:
        """Get one month of the tagged calendar laid out in ISO weeks (Monday → Sunday), with the days counts by kind.

        Args:
            year (int): the Year (2000 → 2040)
            month (int): the Month (1 → 12)

        Returns:
            TaggedMonth: The weeks of the month and the days counts by kind
        """
        return self._fetch(self._month_call(year, month))


class AsyncTaggedCalendarResource(AsyncResourceMixin, TaggedCalendarCalls):
    """Async version of `TaggedCalendarResource`. Same operations, to be awaited."""

    async def year(self, year: int) -> TaggedYear:
        """Get the full tagged calendar of a year. See `TaggedCalendarResource.year`"""
        return await self._fetch(self._year_call(year))

    async def month(self, year: int, month: int) -> TaggedMonth:
        """Get one month of the tagged calendar. See `TaggedCalendarResource.month`"""
        return await self._fetch(self._month_call(year, month))
