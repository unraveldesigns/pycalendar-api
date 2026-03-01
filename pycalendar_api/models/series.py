from dataclasses import dataclass, field
from datetime import date

from sortedcollections import SortedSet

from pycalendar_api.properties import CalFreq
from pycalendar_api.utils import to_date


@dataclass
class DateSeries:
    ref: str
    min_date: date = None
    max_date: date = None
    freq: CalFreq = None
    nitems: int = None
    serie: SortedSet[date] = field(default_factory=SortedSet)

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "DateSeries":
        return cls(**data)

    def __post_init__(self):
        if not isinstance(self.serie, SortedSet) and self.serie:
            self.serie = SortedSet(to_date(x) for x in self.serie)

        if self.freq:
            self.freq = CalFreq(self.freq)

        if self.serie:
            self.nitems = len(self.serie)
            if not self.min_date:
                self.min_date = to_date(min(self.serie))
            if not self.max_date:
                self.max_date = to_date(max(self.serie))

    def __getitem__(self, index: int):
        return self.serie.__getitem__(index)

    def __iter__(self):
        return self.serie.__iter__()

    def __len__(self) -> int:
        return self.serie.__len__()

    def __bool__(self) -> bool:
        return bool(self.serie)

    def __contains__(self, value) -> bool:
        return self.serie.__contains__(value)
