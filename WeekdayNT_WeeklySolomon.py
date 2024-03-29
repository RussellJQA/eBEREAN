"""
A consolidation of several Bible Reading plans:
    WeeklyNT
    WeeklySolomon
"""

from lib.bible_books import bible_books

from create_bible_plan import create_plan_with_playlists

from WeekdayNT import WeekdayNT
from WeeklySolomon import WeeklySolomon

bible_books_list = list(bible_books.keys())


def main():
    daily_readings = {}
    YEAR = 2020
    WeekdayNT(daily_readings, YEAR)
    WeeklySolomon(daily_readings, YEAR, "Sat")  # Saturdays with Solomon
    # for cal_date, full_refs in sorted(daily_readings.items()):
    #     print(cal_date, full_refs)  # Useful for debugging
    create_plan_with_playlists("WeekdayNT_WeeklySolomon", daily_readings)


if __name__ == "__main__":
    main()
