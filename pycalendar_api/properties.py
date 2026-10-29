from collections.abc import Sequence
from enum import StrEnum
from typing import Self


class CalHolidayType(StrEnum):
    """Holidays are categorized under three categories:

        - **ND**: Behaves like Null, Disable this filter
        - **Religious**: Include only Religious holidays. i.e: Eid el fitr, ...
        - **National**: Include only National holidays. i.e: Fête du travail, Fête du trône, ...
        - **Exceptional**: Include only Exceptional holidays
    """
    ND = "ND"
    RELIGIOUS = "Religious"
    NATIONAL = "National"
    EXCEPTIONAL = "Exceptional"


class CalHolidayStatus(StrEnum):
    """Represents the status of religious holidays which are based on moon sightings.

    At the start of the year, Religious holydays are **Estimated**. When the official moon sighting is confirmed the status is changed to **Official**

    NB: The change may **shift the `Estimated` date by ONE DAY**

    All other Holiday types are Official by default

    Attributes:
        - ND: Not defined for the entity or unknown by us (very unlikely)
        - Official (str): The holiday is validated and thus Official
        - Estimated (str): The holiday is estimated before the moon sighting
    """
    ND = "ND"
    ESTIMATED = 'Estimated'
    OFFICIAL = 'Official'


class DayKind(StrEnum):
    """Kind of a day of the Tagged Calendar. Every day has exactly one kind:

        - **ND**: Behaves like Null, Disable this filter
        - **BUSINESS**: The day is an open business day
        - **WEEKEND**: The day is a Saturday or a Sunday. A holiday falling on a weekend is a `WEEKEND`
        - **HOLIDAY**: The day is a holiday falling on a weekday
    """
    ND = "ND"
    BUSINESS = "BUSINESS"
    WEEKEND = "WEEKEND"
    HOLIDAY = "HOLIDAY"


class CalMode(StrEnum):

    """The Mode used by the Fin Calendar to calulate the reference dates of dynamic periods. i.e: 3:M, 23:W, 12:Y, ...

    Enums:
    - D: The calculation is based on open `dailies` dates. Similar to any Business days based calendar
    - W: The calculation is based on the `weeklies` (**Fridays**). Returns the last weekdate related to the provided `period`
    """
    DAILY = "D"
    WEEKLY = "W"

    @classmethod
    def align_mode_calendar(cls, *modes_calendars: Sequence[Self]):
        """Aligne les mode des calendriers selon la fréquence qu'il repésente
        Un DAILY peut être représenté par l'WEEKLY
        Mais l'WEEKLY ne peut être présent sur toutes les dates du DAILY
        """
        if all(x == cls.DAILY for x in modes_calendars):
            return cls.DAILY

        return cls.WEEKLY


class CalFreq(StrEnum):

    """Frequency

    Enums:
        - D: DAILY
        - W: WEEKLY
        - M: MONTHLY
        - Q: QUARTERLY
        - S: SEMI-ANNUALLY
        - Y: YEARLY
    """
    ND = "ND"
    DAILY = "D"
    WEEKLY = "W"
    MONTHLY = "M"
    QUARTERLY = "Q"
    SEMIANNUALLY = "S"
    YEARLY = "Y"

    @classmethod
    def ordered(cls, as_str: bool=False) -> tuple["CalFreq"]:
        gen = (m for m in cls if m != "ND")
        if as_str:
            return tuple(str(m) for m in gen)

        return tuple(gen)


class CalStep(StrEnum):
    """Supported steps for dynamic periods following the format Number:Step

    Steps Values:
        'D': Days: 180:D => 180 Days
        'M': Months: 6:M => 6 Months
        'W': Weeks: 26:W => 26 Weeks
        'Y': Years: 2:Y => 2 Years
    """
    D = 'D'
    M = 'M'
    W = 'W'
    Y = 'Y'
