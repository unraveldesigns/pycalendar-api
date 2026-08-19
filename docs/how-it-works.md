# How it works

## Religious holidays

Religious holidays are `Official` when the moon sightings confirm it, therefore all future `Religious` holidays are estimated.

Once confirmed, the status of the `HolidayStatus` changes to `HolidayStatus.OFFICIAL`.

## National holidays

National holidays are defined in the gregorian calendar.

## Kingdom days

Since Morocco is a Kingdom (Royaume du Maroc), there are holidays which depend on the birthday of the current King and the day of his coronation.

## Weekends

Weekends (Saturday and Sunday) are considered as holidays in our API, but they are not returned in the response.
Officially only the Sunday is a dayoff, but since the whole economy works from Monday - Friday, we decided to consider them both for a better user/developper experience.

## Data Model

All Holidays follow the `SCD Type 2` approach for keeping the history. The implication is that you won't find Holidays when they weren't defined.

## History

Religious holidays are qualidfied since **2006**. More years will be added up to **1985**.

<script defer src="https://odometer.calendar-api.ma/script.js" data-website-id="3b3a9e56-7e3a-4c20-b6b4-fce013629789" data-tag="docs"></script>
