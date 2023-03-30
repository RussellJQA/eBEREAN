"""
Create a Bible reading plan with 104 readings from the Psalms, 1 for each weekend day.
Although the readings themselves are taken directly from the Bible Reading Plan of
Robert Murray M‘Cheyne (1813-1843), this plan orders them quite differently.

"""

import calendar
import datetime

from lib.bible_books import bible_books
from lib.rmm_psalm_readings import rmm_original_104_psalm_readings

from create_bible_plan import create_plan_with_playlists, get_weekday, process_reading

bible_books_list = list(bible_books.keys())


def WeekendPsalms(daily_readings, year):  # Weekend Worship (Psalms)
    def get_num_extra_readings():
        num_extra_readings = 0
        if get_weekday(datetime.datetime(year, 12, 31)) in ("Sat", "Sun"):
            num_extra_readings += 1  # Increment if December 31 is on a weekend
        if calendar.isleap(year) and (
            get_weekday(datetime.datetime(year, 12, 30)) in ("Sat", "Sun")
        ):
            num_extra_readings += (
                1  # Increment if leap year & December 30 is on a weekend
            )
        # print(f'For {year}, {num_extra_readings} extra WeekendPsalms() readings are needed.')
        return num_extra_readings

    date = datetime.datetime(year, 1, 1)  # January 1
    while get_weekday(date) not in ("Sat", "Sun"):
        date += datetime.timedelta(days=1)  # Increment until first weekend day

    for psalm_ref in rmm_original_104_psalm_readings:
        datedelta = 6 if (get_weekday(date) == "Sun") else 1
        # If date is a Lord's Day, then increment date to the following Saturday
        # Else {date is a Saturday} increment date to the next day (a Lord's Day)
        (daily_readings, date) = process_reading(
            daily_readings, date, "Psa", psalm_ref, datedelta
        )

    extra_psalm_refs = ["23", "100"]  # Up to 2 extra readings
    for i in range(get_num_extra_readings()):
        datedelta = 6 if (get_weekday(date) == "Sun") else 1
        (daily_readings, date) = process_reading(
            daily_readings, date, "Psa", extra_psalm_refs[i], datedelta
        )


def main():
    daily_readings = {}
    YEAR = 2020
    WeekendPsalms(daily_readings, YEAR)
    # for cal_date, full_refs in sorted(daily_readings.items()):
    #     print(cal_date, full_refs)  # Useful for debugging
    create_plan_with_playlists("WeekendPsalms", daily_readings)


if __name__ == "__main__":
    main()
