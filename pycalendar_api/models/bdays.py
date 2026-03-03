import datetime
from dataclasses import dataclass

from pycalendar_api.properties import CalFreq
from pycalendar_api.utils import to_date


@dataclass
class DaysCount:
    start_date: datetime.date = None
    end_date: datetime.date = None
    count: int = None
    freq: CalFreq = None

    def __post_init__(self):
        if self.start_date:
            self.start_date = to_date(self.start_date)
        if self.end_date:
            self.end_date = to_date(self.end_date)
        if self.freq:
            self.freq = CalFreq(self.freq)

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "DaysCount":
        return cls(**data)


@dataclass
class CalSpan:
    start_date: datetime.date = None
    end_date: datetime.date = None
    year: int = None
    semester: int = None
    quarter: int = None
    month: int = None
    country_code: str = "MA"

    def __post_init__(self):
        if self.start_date:
            self.start_date = to_date(self.start_date)
        if self.end_date:
            self.end_date = to_date(self.end_date)

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "CalSpan":
        return cls(**data)

    @property
    def key(self) -> str:
        """A Unique key to identify the span. Takes the form of {year}-{span}{span-number}.

        i.e: "2025-Q3", 2025-S1, 2025-M8
        """
        rv = str(self.year)
        if self.semester:
            return rv + f"-S{self.semester}"
        if self.quarter:
            return rv + f"-Q{self.quarter}"
        if self.month:
            return rv + f"-M{self.month}"
        return rv


@dataclass
class NextDate:
    date: datetime.date
    next_date: datetime.date

    def __post_init__(self):
        if self.date:
            self.date = to_date(self.date)
        if self.next_date:
            self.next_date = to_date(self.next_date)

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "NextDate":
        return cls(**data)


@dataclass
class PreviousDate:
    date: datetime.date
    previous_date: datetime.date

    def __post_init__(self):
        if self.date:
            self.date = to_date(self.date)
        if self.previous_date:
            self.previous_date = to_date(self.previous_date)

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "PreviousDate":
        return cls(**data)
