"""
Create a Bible reading plan with 104 readings from the Psalms, 1 for each weekend day.
Although the readings themselves are taken directly from the Bible Reading Plan of
Robert Murray M‘Cheyne (1813-1843), this plan orders them quite differently.

"""

import calendar
import datetime
import os

from bible_books import bible_books
from rmm_psalm_readings import rmm_original_104_psalm_readings
from create_bible_plan import create_plan_with_playlists, get_weekday, process_reading

bible_books_list = list(bible_books.keys())


def WeekendPsalms(daily_readings, year):  # Weekend Worship (Psalms)

    date = datetime.datetime(year, 1, 1)  # January 1
    while get_weekday(date) not in ("Sat", "Sun"):
        date += datetime.timedelta(days=1)  # Increment until first weekend day

    # TODO: Add needed extra readings.
    #       For years other than 2020, the readings themselves may need to be adjusted.
    # extra_readings = 0
    # if (get_weekday(datetime.datetime(year, 12, 31)) in ('Sat', 'Sun')):
    #     extra_readings += 1  # Increment if December 31 is on a weekend
    # if (calendar.isleap(year) and
    #     (get_weekday(datetime.datetime(year, 12, 30)) in ('Sat', 'Sun'))):
    #     extra_readings += 1  # Increment if leap year & December 30 is on a weekend
    # print(f'For {year}, {extra_readings} extra WeekendPsalms() readings are needed.')

    for count, psalm_ref in enumerate(rmm_original_104_psalm_readings):
        datedelta = 6 if (count % 2) else 1
        # If date is a Lord's Day, then increment date to the following Saturday
        # Else {date is a Saturday} increment date to the next day (a Lord's Day)
        (daily_readings, date) = process_reading(
            daily_readings, date, "Psa", psalm_ref, datedelta
        )

    return daily_readings


def main():
    daily_readings = {}
    YEAR = 2020
    WeekendPsalms(daily_readings, YEAR)
    # for cal_date, full_refs in sorted(daily_readings.items()):
    #     print(cal_date, full_refs)  # Useful for debugging
    create_plan_with_playlists("WeekendPsalms", daily_readings)


if __name__ == "__main__":
    main()
