"""
A consolidation of several Bible Reading plans:
    WeekdayPsalms
    WeekendPsalms
    WeeklyNT
    DailyOTDuo
    WeeklySolomon
"""

import calendar
import datetime
import os

from lib.bible_books import bible_books

from create_bible_plan import create_plan_with_playlists, get_weekday, process_reading

from WeekdayPsalms import WeekdayPsalms
from WeekendPsalms import WeekendPsalms
from WeekdayNT import WeekdayNT
from WeeklySolomon import WeeklySolomon

bible_books_list = list(bible_books.keys())

solomon = ["Proverbs", "Ecclesiastes", "SongOfSolomon"]


def DailyOTDuo(daily_readings, year):
    # Daily OT Duo (OT without Psalms and without Solomon's Writings)

    # TODO: Move into separate file.

    date = datetime.datetime(year, 1, 1)  # January 1

    def get_readings():
        def get_num_extra_readings():
            num_extra_readings = 4 if calendar.isleap(year) else 2
            # print(f"{num_extra_readings} extra OTMain readings needed for {year}.")
            return num_extra_readings

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

        substitutions = [
            ["Num 7", ["Num 7:1-47", "Num 7:48-89"]],
            ["1Ch 6", ["1Ch 6:1-48", "1Ch 6:49-81"]],
            ["Neh 7", ["Neh 7:1-38", "Neh 7:39-73"]],
            ["Ezr 2", ["Ezr 2:1-36", "Ezr 2:37-70"]],
        ]  # Split (when needed) 1-4 of the 4 longest OT chapters
        #    (excluding Psalms and Solomon's writings)

        for i in range(get_num_extra_readings()):
            substitution = substitutions.pop(0)
            index = readings.index(substitution[0])
            readings[index : index + 1] = substitution[1]

        return readings

    chapter_count = 0
    for reading in get_readings():
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
    DailyOTDuo(daily_readings, YEAR)
    WeeklySolomon(daily_readings, YEAR, "Sat")  # Saturdays with Solomon
    # for cal_date, full_refs in sorted(daily_readings.items()):
    #     print(cal_date, full_refs)  # Useful for debugging
    create_plan_with_playlists("WeekdayNTPlus", daily_readings)


if __name__ == "__main__":
    main()
