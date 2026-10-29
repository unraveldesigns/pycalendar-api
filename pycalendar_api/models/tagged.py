import datetime
from collections.abc import Iterator
from dataclasses import dataclass, field

from pycalendar_api.properties import CalHolidayStatus, CalHolidayType, DayKind
from pycalendar_api.utils import to_date


@dataclass
class TaggedDay:
    """A day of the Tagged Calendar, tagged with its `day_kind`.

    `holiday_type`, `status` and `description` are only defined when `is_holiday` is True.
    A holiday falling on a weekend has `is_holiday=True` and `day_kind=DayKind.WEEKEND`.
    """
    date: datetime.date = None
    day_kind: DayKind = None
    is_business_day: bool = None
    is_weekend: bool = None
    is_holiday: bool = None
    holiday_type: CalHolidayType = None
    status: CalHolidayStatus = None
    description: str = None
    label: str = None
    country_code: str = "MA"

    def __post_init__(self):
        if self.date:
            self.date = to_date(self.date)
        if self.day_kind:
            self.day_kind = DayKind(self.day_kind)
        if self.holiday_type:
            self.holiday_type = CalHolidayType(self.holiday_type)
        if self.status:
            self.status = CalHolidayStatus(self.status)

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "TaggedDay":
        return cls(**data)


@dataclass
class TaggedDaysCount:
    """Number of days by `day_kind`. The sum equals the number of days of the period.

    A holiday falling on a weekend is counted in `weekend_days`
    """
    business_days: int = None
    weekend_days: int = None
    holidays: int = None

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "TaggedDaysCount":
        return cls(**data)

    @property
    def total(self) -> int:
        """Number of days of the period"""
        return self.business_days + self.weekend_days + self.holidays


@dataclass
class TaggedMonth:
    """A month of the Tagged Calendar laid out in ISO weeks (Monday → Sunday), ready to be rendered as a calendar grid.

    `weeks` is a list of 7 days lists, the days outside the month are `None`. `weekday_labels` are the column headers (MO → SU).
    """
    year: int = None
    month: int = None
    label: str = None
    weekday_labels: list[str] = field(default_factory=list)
    counts: TaggedDaysCount = None
    weeks: list[list[TaggedDay | None]] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.counts, dict):
            self.counts = TaggedDaysCount.from_json(self.counts)
        self.weeks = [
            [TaggedDay.from_json(d) if isinstance(d, dict) else d for d in week]
            for week in self.weeks
        ]

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "TaggedMonth":
        return cls(**data)

    @property
    def days(self) -> list[TaggedDay]:
        """Ordered days of the month, without the `None` padding of the weeks"""
        return [d for week in self.weeks for d in week if d is not None]

    def __iter__(self) -> Iterator[TaggedDay]:
        return iter(self.days)


@dataclass
class TaggedYear:
    """A full year of the Tagged Calendar, month by month"""
    year: int = None
    counts: TaggedDaysCount = None
    months: list[TaggedMonth] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.counts, dict):
            self.counts = TaggedDaysCount.from_json(self.counts)
        self.months = [TaggedMonth.from_json(m) if isinstance(m, dict) else m for m in self.months]

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "TaggedYear":
        return cls(**data)

    @property
    def days(self) -> list[TaggedDay]:
        """Ordered days of the year"""
        return [d for m in self.months for d in m.days]

    def __iter__(self) -> Iterator[TaggedDay]:
        return iter(self.days)

    def month(self, month: int) -> TaggedMonth:
        """Get a month of the year

        Args:
            month (int): Month number (1 → 12)

        Raises:
            KeyError: Month not in the year
        """
        for m in self.months:
            if m.month == month:
                return m
        raise KeyError(month)
