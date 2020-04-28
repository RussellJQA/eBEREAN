"""
A consolidation of several Bible Reading plans:
    WeekdayPsalms
    WeekendPsalms
    WeeklyNT
    DailyOTDuo
    WeeklySolomon
"""

from lib.bible_books import bible_books

from create_bible_plan import create_plan_with_playlists

from WeekdayPsalms import WeekdayPsalms
from WeekendPsalms import WeekendPsalms
from WeekdayNT import WeekdayNT
from DailyOTDuo import DailyOTDuo
from WeeklySolomon import WeeklySolomon

bible_books_list = list(bible_books.keys())

solomon = ["Proverbs", "Ecclesiastes", "SongOfSolomon"]


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
