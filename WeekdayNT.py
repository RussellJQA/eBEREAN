"""
Create a Bible reading plan with 1 of the 260 NT chapters for every weekday of the year.
For years with more than 260 (52*5) weekdays, 1 or more chapters are split over 2 days.
"""

import calendar
import datetime
import os

from bible_books import bible_books
from create_bible_plan import (
    create_plan_with_playlists,
    get_weekday,
    get_weekday_delta,
    process_reading,
)

bible_books_list = list(bible_books.keys())


def WeekdayNT(daily_readings, year):  # Weekday New Testament
    date = datetime.datetime(year, 1, 1)  # January 1
    while date.strftime("%a") in ("Sat", "Sun"):
        date += datetime.timedelta(days=1)  # Increment until first weekday

    # TODO: Change this and similar functions to use classes/subclasses.

    def get_readings():

        def get_num_extra_readings():
            num_extra_readings = 0
            if get_weekday(datetime.datetime(year, 12, 31)) not in ("Sat", "Sun"):
                num_extra_readings += 1  # Increment if December 31 is a weekday
            if calendar.isleap(year) and (
                get_weekday(datetime.datetime(year, 12, 30)) not in ("Sat", "Sun")
            ):
                num_extra_readings += 1  # Increment if leap year & December 30 is a weekday
            # print(f'{num_extra_readings} extra WeekdayNT readings needed for {year}')
            return num_extra_readings

        substitutions = [
            ["Luk 1", ["Luk 1:1-38", "Luk 1:39-80"]],
            ["Mat 26", ["Mat 26:1-35", "Mat 26:36-75"]],
        ]  # Split (when needed) 1 or 2 of the 2 longest NT chapters

        readings = []
        for book in bible_books_list[
            bible_books_list.index("Matthew") : bible_books_list.index("Revelation") + 1
        ]:
            book_abbr, book_chapters = bible_books[book]
            for chapter in range(1, book_chapters + 1):
                readings.append(book_abbr + " " + str(chapter))

        for i in range(get_num_extra_readings()):
            substitution = substitutions.pop(0)
            index = readings.index(substitution[0])
            readings[index : index + 1] = substitution[1]

        return readings

    readings = get_readings()
    for reading in readings:
        book_abbr, chapter = reading.split()
        datedelta = get_weekday_delta(date)
        (daily_readings, date) = process_reading(
            daily_readings, date, book_abbr, chapter, datedelta
        )

    return daily_readings


def main():
    daily_readings = {}
    YEAR = 2020
    WeekdayNT(daily_readings, YEAR)
    # for cal_date, full_refs in sorted(daily_readings.items()):
    #     print(cal_date, full_refs)  # Useful for debugging
    create_plan_with_playlists("WeekdayNT", daily_readings)


if __name__ == "__main__":
    main()
