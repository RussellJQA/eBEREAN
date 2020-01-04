"""
A consolidation of several Bible Reading plans:
    WeeklyNT
    WeeklySolomon
    OTDailyDuo
    WeekdayPsalms
    WeekendPsalms
"""

import calendar
import datetime

from bible_books import bible_books
from create_bible_plan import (
    get_weekday,
    get_weekday_delta,
    print_daily_reading,
    process_reading,
)
from create_daily_bible_reading_play_list import create_daily_bible_reading_play_list

from psalm_readings import weekend_psalm_readings, weekday_psalm_readings
from WeekendPsalms import WeekendPsalms
from WeekdayNT import WeekdayNT
from WeeklySolomon import WeeklySolomon

bible_books_list = list(bible_books.keys())

solomon = ["Proverbs", "Ecclesiastes", "SongOfSolomon"]


def WeekdayPsalms(daily_readings, year):  # Weekday Worship (Psalms)
    date = datetime.datetime(year, 1, 1)  # January 1
    while date.strftime("%a") in ("Sat", "Sun"):
        date += datetime.timedelta(days=1)  # Increment until first weekday

    # TODO: Add needed extra readings.
    #       For years other than 2020, the readings themselves may need to be adjusted.
    # extra_readings = 0
    # if (get_weekday(datetime.datetime(year, 12, 31)) not in ('Sat', 'Sun')):
    #     extra_readings += 1  # Increment if December 31 is a weekday
    # if (calendar.isleap(year) and
    #     (get_weekday(datetime.datetime(year, 12, 30)) not in ('Sat', 'Sun'))):
    #     extra_readings += 1  # Increment if leap year & December 30 is a weekday
    # print(f'For {year}, {extra_readings} extra WeekdayPsalms() readings are needed.')

    for count, psalm_ref in enumerate(weekday_psalm_readings):
        datedelta = get_weekday_delta(date)
        (daily_readings, date) = process_reading(
            daily_readings, date, "Psa", psalm_ref, datedelta
        )

    return daily_readings


def OTMain(daily_readings, year):
    # Daily OT Duo (OT without Psalms and without Solomon's Writings)
    date = datetime.datetime(year, 1, 1)  # January 1

    substitutions = [
        ["Num 7", ["Num 7:1-47", "Num 7:48-89"]],
        ["1Ch 6", ["1Ch 6:1-48", "1Ch 6:49-81"]],
        ["Neh 7", ["Neh 7:1-38", "Neh 7:39-73"]],
        ["Ezr 2", ["Ezr 2:1-36", "Ezr 2:37-70"]],
    ]  # Split (when needed) 1-4 of the 4 longest OT chapters
    #    (excluding Psalms and Solomon's writings)

    def get_num_extra_readings():
        num_extra_readings = 4 if calendar.isleap(year) else 2
        # print(f"{num_extra_readings} extra OTMain readings are needed for {year}.")
        return num_extra_readings

    def get_readings(num_extra_readings):
        readings = []

        ot_without_psalms_and_solomon = bible_books_list[
            bible_books_list.index("Genesis") : bible_books_list.index("Malachi") + 1
        ]
        ot_without_psalms_and_solomon.remove("Psalms")
        for book in solomon:
            ot_without_psalms_and_solomon.remove(book)

        for book in ot_without_psalms_and_solomon:
            book_abbr, book_chapters = bible_books[book]
            for chapter in range(1, book_chapters + 1):
                readings.append(book_abbr + " " + str(chapter))
        for i in range(num_extra_readings):
            substitution = substitutions.pop(0)
            index = readings.index(substitution[0])
            readings[index : index + 1] = substitution[1]
        return readings

    readings = get_readings(get_num_extra_readings())
    chapter_count = 0
    for reading in readings:
        chapter_count += 1
        book_abbr, chapter = reading.split()
        datedelta = 0 if (chapter_count % 2) else 1  # Increment on every other chapter
        merge_refs = not (chapter_count % 2)  # Merge references on every other chapter
        (daily_readings, date) = process_reading(
            daily_readings, date, book_abbr, chapter, datedelta, merge_refs
        )

    return daily_readings


def main():
    daily_readings = {}
    YEAR = 2020
    WeekdayPsalms(daily_readings, YEAR)
    WeekendPsalms(daily_readings, YEAR)
    WeekdayNT(daily_readings, YEAR)
    OTMain(daily_readings, YEAR)
    WeeklySolomon(daily_readings, YEAR, "Sat")  # Saturdays with Solomon

    # for cal_date, full_refs in sorted(daily_readings.items()):
    #     print(cal_date, full_refs)  # Useful for debugging

    previous_month = ""
    for (cal_date, full_refs) in sorted(daily_readings.items()):
        # items() returns a list of (key, value) tuples
        previous_month = print_daily_reading(cal_date, previous_month, full_refs)
        create_daily_bible_reading_play_list(cal_date, full_refs)


if __name__ == "__main__":
    main()
