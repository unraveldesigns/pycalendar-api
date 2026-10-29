# How it works

## Religious holidays

Religious holidays are `Official` when the moon sightings confirm it, therefore all future `Religious` holidays are estimated.

Once confirmed, the status of the `HolidayStatus` changes to `HolidayStatus.OFFICIAL`.

## National holidays

National holidays are defined in the gregorian calendar.

## Kingdom days

Since Morocco is a Kingdom (Royaume du Maroc), there are holidays which depend on the birthday of the current King and the day of his coronation.

## Weekends

Weekends (Saturday and Sunday) are considered as days off in our API. The Holidays and Business days endpoints do not return them,
the Tagged Calendar returns them tagged as `WEEKEND`.
Officially only the Sunday is a dayoff, but since the whole economy works from Monday - Friday, we decided to consider them both for a better user/developper experience.

## Tagged Calendar

The Tagged Calendar merges the Holidays and the Business days in a single view: every day of the period is returned with one `DayKind`.

- `BUSINESS`: an open business day (`is_business_day=True`)
- `WEEKEND`: a Saturday or a Sunday. **A holiday falling on a weekend is a `WEEKEND`**, it keeps `is_holiday=True`, its type, status and description
- `HOLIDAY`: a holiday falling on a weekday

Thanks to this rule, the `counts` by kind (`business_days + weekend_days + holidays`) always equal the number of days of the period.

Each month is laid out in **ISO weeks** (Monday → Sunday) with `weekday_labels` as column headers; the days of the previous and next months are `None`, so `weeks` can be rendered directly as a calendar grid.
`label` is a ready to display text, ie: `Jan 14 — Nouvel an amazigh`, `Jan 3 — Weekend`, `Jan 5 — Business day`. An estimated religious holiday ends with ` (estimated)`.

Like the Holidays endpoints, exceptional holidays are not exposed, those days are tagged as regular days.
The Tagged Calendar covers the years **2000 → 2040**.

## Data Model

All Holidays follow the `SCD Type 2` approach for keeping the history. The implication is that you won't find Holidays when they weren't defined.

## History

Religious holidays are qualidfied since **2006**. More years will be added up to **1985**.

<script defer src="https://odometer.calendar-api.ma/script.js" data-website-id="3b3a9e56-7e3a-4c20-b6b4-fce013629789" data-tag="docs"></script>
