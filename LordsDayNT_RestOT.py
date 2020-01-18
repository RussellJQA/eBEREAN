"""
This Bible reading plan has the reader read:
    Lord's Days: 5 New Testament chapters
    Other Days: 3 Old Test chapters (or portions)

This is a work in progress, not yet as fully implemented as the other reading plans.
"""

import calendar
import datetime
import os

from lib.bible_books import bible_books

from create_bible_plan import create_plan_with_playlists, get_weekday, process_reading

bible_books_list = list(bible_books.keys())


def LordsDayNT(daily_readings, year):

    date = datetime.datetime(year, 1, 1)  # January 1
    while date.strftime("%a") != "Sun":
        date += datetime.timedelta(days=1)  # Increment until Lord's Day

    def get_readings():

        readings = []

        nt_books = bible_books_list[
            bible_books_list.index("Matthew") : bible_books_list.index("Revelation") + 1
        ]
        for book in nt_books:
            book_abbr, book_chapters = bible_books[book]
            for chapter in range(1, book_chapters + 1):
                readings.append(book_abbr + " " + str(chapter))

        return readings

    chapter_count = 0
    for reading in get_readings():
        chapter_count += 1
        book_abbr, chapter = reading.split()
        datedelta = 0 if (chapter_count % 5) else 7
        # Every 5th chapter, increment to next Lord's Day

        # TODO: Properly handle merging of up to 5 references
        # (5 NT chapters each Lord's Day)
        (daily_readings, date) = process_reading(
            daily_readings, date, book_abbr, chapter, datedelta
        )

    return daily_readings


def Rest_OT(daily_readings, year):
    # 3 OT chapters on every day other than the Lord's Day

    date = datetime.datetime(year, 1, 1)  # January 1
    if date.strftime("%a") == "Sun":
        date += datetime.timedelta(days=1)  # Skip Lord's Day

    def get_readings():

        readings = []

        ot_books = bible_books_list[
            bible_books_list.index("Genesis") : bible_books_list.index("Malachi") + 1
        ]
        for book in ot_books:
            book_abbr, book_chapters = bible_books[book]
            for chapter in range(1, book_chapters + 1):
                readings.append(book_abbr + " " + str(chapter))

        ps119_index = readings.index("Psa 119")
        readings[ps119_index : ps119_index + 1] = [
            "Psa 119:1-24",
            "Psa 119:25-48",
            "Psa 119:49-72",
            "Psa 119:73-96",
            "Psa 119:97-120",
            "Psa 119:121-144",
            "Psa 119:145-160",
            "Psa 119:161-176",
        ]  # Split Psalm 119 for 52*6=312 total readings

        return readings

    chapter_count = 0
    for reading in get_readings():
        chapter_count += 1
        book_abbr, chapter = reading.split()
        datedelta = 0
        if not (chapter_count % 3):  # Increment on every third chapter
            datedelta = (
                2 if (get_weekday(date) == "Sat") else 1
            )  # Skip over Lord's Days
        # TODO: Merge similar references
        (daily_readings, date) = process_reading(
            daily_readings, date, book_abbr, chapter, datedelta
        )

    return daily_readings


def main():
    daily_readings = {}
    YEAR = 2020
    LordsDayNT(daily_readings, YEAR)
    Rest_OT(daily_readings, YEAR)

    # TODO: Add extra readings (such as metrical Psalms, with their
    #       corresponding prose Psalms) to handle:
    #           day 365: for all years
    #           day 366: for leap years

    # for cal_date, full_refs in sorted(daily_readings.items()):
    #     print(cal_date, full_refs)  # Useful for debugging
    create_plan_with_playlists("LordsDayNT_RestOT", daily_readings)


if __name__ == "__main__":
    main()
