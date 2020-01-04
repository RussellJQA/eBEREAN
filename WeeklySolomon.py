"""
Create a Bible reading plan with 1 of the 51 chapters from Solomon's writings
(including Ecclesiastes) for every week of the year, with 1 or more chapters
split over 2 days (as needed).
"""

import calendar
import datetime

from bible_books import bible_books
from create_bible_plan import (
    print_daily_reading,
    process_reading,
)
from create_daily_bible_reading_play_list import create_daily_bible_reading_play_list


bible_books_list = list(bible_books.keys())

solomon = ["Proverbs", "Ecclesiastes", "SongOfSolomon"]


def WeeklySolomon(daily_readings, year, day_of_week):  # Weekly Solomon's Readings
    # Proverbs, Ecclesiastes, and SongOfSolomon

    date = datetime.datetime(year, 1, 1)  # January 1
    while date.strftime("%a") != day_of_week:
        date += datetime.timedelta(days=1)  # Increment until specified day_of_week

    substitutions = [
        ["Pro 8", ["Pro 8:1-18", "Pro 8:19-36"]],
        ["Pro 23", ["Pro 23:1-18", "Pro 23:19-35"]],
    ]  # Split (when needed) 1 or 2 of the 2 longest Weekly Wisdom chapters

    def get_num_extra_readings():
        num_extra_readings = 1  # There are only 51 chapters in Pro thru Ecc
        if (date + datetime.timedelta(days=52 * 7)) <= datetime.datetime(year, 12, 31):
            # if (52 weeks from start date) is before or on December 31, then ...
            num_extra_readings += 1
        # print(f'{num_extra_readings} extra WeeklyWisdom readings are needed for {year} ({day_of_week})')
        return num_extra_readings

    def get_readings(num_extra_readings):
        readings = []
        for book in solomon:
            book_abbr, book_chapters = bible_books[book]
            for chapter in range(1, book_chapters + 1):
                readings.append(book_abbr + " " + str(chapter))
        for i in range(num_extra_readings):
            substitution = substitutions.pop(0)
            index = readings.index(substitution[0])
            readings[index : index + 1] = substitution[1]
        return readings

    readings = get_readings(get_num_extra_readings())
    for reading in readings:
        book_abbr, chapter = reading.split()
        (daily_readings, date) = process_reading(
            daily_readings, date, book_abbr, chapter, 7
        )

    return daily_readings


def main():
    daily_readings = {}
    YEAR = 2020
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
