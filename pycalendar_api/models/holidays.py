import datetime
from dataclasses import dataclass

from pycalendar_api.properties import CalHolidayStatus, CalHolidayType
from pycalendar_api.utils import to_date


@dataclass
class Holiday:
    description: str = None
    day: int = None
    month: int = None
    date: datetime.date = None
    holiday_type: CalHolidayType = None
    status: CalHolidayStatus = None
    country_code: str = "MA"

    def __post_init__(self):
        if self.date:
            self.date = to_date(self.date)
        if self.holiday_type:
            self.holiday_type = CalHolidayType(self.holiday_type)
        if self.status:
            self.status = CalHolidayStatus(self.status)

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "Holiday":
        return cls(**data)


@dataclass
class HolidayCheckResult:
    date: datetime.date = None
    is_holiday: bool = None
    description: str = None
    holiday_type: CalHolidayType = None
    status: CalHolidayStatus = None
    country_code: str = "MA"

    def __post_init__(self):
        if self.date:
            self.date = to_date(self.date)
        if self.holiday_type:
            self.holiday_type = CalHolidayType(self.holiday_type)
        if self.status:
            self.status = CalHolidayStatus(self.status)

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "HolidayCheckResult":
        return cls(**data)
