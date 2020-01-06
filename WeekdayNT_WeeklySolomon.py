"""
A consolidation of several Bible Reading plans:
    WeeklyNT
    WeeklySolomon
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
from create_bible_plan_playlists import create_bible_plan_playlists

from WeekdayNT import WeekdayNT
from WeeklySolomon import WeeklySolomon

bible_books_list = list(bible_books.keys())

solomon = ["Proverbs", "Ecclesiastes", "SongOfSolomon"]

def main():
    daily_readings = {}
    YEAR = 2020
    WeekdayNT(daily_readings, YEAR)
    WeeklySolomon(daily_readings, YEAR, "Sat")  # Saturdays with Solomon

    # for cal_date, full_refs in sorted(daily_readings.items()):
    #     print(cal_date, full_refs)  # Useful for debugging

    previous_month = ""
    for (cal_date, full_refs) in sorted(daily_readings.items()):
        # items() returns a list of (key, value) tuples
        previous_month = print_daily_reading(cal_date, previous_month, full_refs)
        create_bible_plan_playlists("WeekdayNT_WeeklySolomon", cal_date, full_refs)


if __name__ == "__main__":
    main()
