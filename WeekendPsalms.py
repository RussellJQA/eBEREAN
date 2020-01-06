"""
Create a Bible reading plan with readings from the Psalms for each weekend day.
"""

import calendar
import datetime
import os

from bible_books import bible_books
from create_bible_plan import create_plan_with_playlists, get_weekday, process_reading

bible_books_list = list(bible_books.keys())


def WeekendPsalms(daily_readings, year):  # Weekend Worship (Psalms)

    weekend_psalm_readings = [
        "1-2",
        "3-4",
        "5-6",
        "7-8",
        "9",
        "10",
        "11-12",
        "13-14",
        "15-16",
        "17",
        "18",
        "19",
        "20-21",
        "22",
        "23-24",
        "25",
        "26-27",
        "28-29",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40-41",
        "42-43",
        "44",
        "45",
        "46-47",
        "48",
        "49",
        "50",
        "51",
        "52-54",
        "55",
        "56-57",
        "58-59",
        "60-61",
        "62-63",
        "64-65",
        "66-67",
        "68",
        "69",
        "70-71",
        "72",
        "73",
        "74",
        "75-76",
        "77",
        "78:1-37",
        "78:38-72",
        "79",
        "80",
        "81-82",
        "83-84",
        "85",
        "86-87",
        "88",
        "89",
        "90",
        "91",
        "92-93",
        "94",
        "95-96",
        "97-98",
        "99-101",
        "102",
        "103",
        "104",
        "105",
        "106",
        "107",
        "108-109",
        "110-111",
        "112-113",
        "114-115",
        "116",
        "117-118",
        "119:1-24",
        "119:25-48",
        "119:49-72",
        "119:73-96",
        "119:97-120",
        "119:121-144",
        "119:145-176",
        "120-122",
        "123-125",
        "126-128",
        "129-131",
        "132-134",
        "135-136",
        "137-138",
        "139",
        "140-141",
        "142-143",
        "144",
        "145",
        "146-147",
        "148",
        "149-150",
    ]

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

    for count, psalm_ref in enumerate(weekend_psalm_readings):
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
