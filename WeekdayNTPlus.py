import datetime
import calendar

from bible_data import bible_books, weekend_psalm_readings, weekday_psalm_readings

bible_books_list = list(bible_books.keys())

solomon = ["Proverbs", "Ecclesiastes", "Song of Solomon"]
# Solomon's Proverbial wisdom, the wisdom of the Preacher, and Wisdom and His Wife
# ('Wisdom' being 'One Wiser than Solomon' )

daily_readings = {}


def get_weekday(date):
    return date.strftime("%a")


def get_weekday_delta(date):
    day_of_week = date.strftime("%a")
    if day_of_week == "Fri":
        return 3
    elif day_of_week == "Sat":
        return 2
    else:
        return 1


def process_reading(date, book_abbr, reference, datedelta, merge_refs=False):
    cal_date = date.strftime("%m/%d %a")
    full_ref = book_abbr + " " + reference

    def do_merge_refs():
        last_full_ref = daily_readings[cal_date][-1]
        last_book_abbr = last_full_ref[0 : last_full_ref.find(" ")]

        if last_book_abbr == book_abbr:
            daily_readings[cal_date][-1] += "-" + reference
            # Concatenate new reference to old reference, with a dash separating
            # TODO: Need to update this to properly merge OT split chapter references:
            #   Num 6-7:1-47        => Num 6-7:47
            #   Num 7:48-89-8       => Num 7:48-89;8 {or better, Num 7:48-8:26}
            #   1Ch 6:1-48-6:49-81  => 1Ch 6:1-81 {or better, just 1Ch 6}
            #   Ezr 2:1-36-2:37-70  => Ezr 2:1-70 {or better, just Ezr 2}
            #   Neh 7:1-38-7:39-73  => Neh 7:1-73 {or better, just Neh 7}
            # {Hint 1: Use regular expressions to match ref1/ref2 patterns.}
            # {Hint 2: For "better", lookup chapter length (in verses) for ref2.}
            # For now, I just hand-tweaked these in any output files

        else:
            daily_readings[cal_date][-1] += "-" + full_ref
            # Concatenate new full_ref to old full_ref, with a dash separating

    if cal_date in daily_readings:
        if merge_refs:
            do_merge_refs()
        else:
            daily_readings[cal_date].append(full_ref)
            # Append new full_ref to list of daily readings for this day
    else:
        daily_readings[cal_date] = [full_ref]  # Insert 1st reading for this day

    return date + datetime.timedelta(days=datedelta)


def WeekdayPsalms(year):  # Weekday Worship (Psalms)
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
        date = process_reading(date, "Psa", psalm_ref, get_weekday_delta(date))


def WeekendPsalms(year):  # Weekend Worship (Psalms)
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
        date = process_reading(date, "Psa", psalm_ref, (6 if (count % 2) else 1))
        # If date is a Lord's Day, then increment date to the following Saturday
        # Else {date is a Saturday} increment date to the next day (a Lord's Day)


def WeekdayNT(year):  # Weekday New Testament
    date = datetime.datetime(year, 1, 1)  # January 1
    while date.strftime("%a") in ("Sat", "Sun"):
        date += datetime.timedelta(days=1)  # Increment until first weekday

    # TODO: Change this and similar functions to use classes/subclasses.

    substitutions = [
        ["Luk 1", ["Luk 1:1-38", "Luk 1:39-80"]],
        ["Mat 26", ["Mat 26:1-35", "Mat 26:36-75"]],
    ]  # Split (when needed) 1 or 2 of the 2 longest NT chapters

    def get_num_extra_readings():
        num_extra_readings = 0
        if get_weekday(datetime.datetime(year, 12, 31)) not in ("Sat", "Sun"):
            num_extra_readings += 1  # Increment if December 31 is a weekday
        if calendar.isleap(year) and (
            get_weekday(datetime.datetime(year, 12, 30)) not in ("Sat", "Sun")
        ):
            num_extra_readings += 1  # Increment if leap year & December 30 is a weekday
        # print(f'{num_extra_readings} extra WeekdayNT readings are needed for {year}')
        return num_extra_readings

    def get_readings(num_extra_readings):
        readings = []
        for book in bible_books_list[
            bible_books_list.index("Matthew") : bible_books_list.index("Revelation") + 1
        ]:
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
        date = process_reading(date, book_abbr, chapter, get_weekday_delta(date))


def OTMain(year):  # Daily OT Duo (OT without Psalms and without Solomon's Writings)
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
        date = process_reading(date, book_abbr, chapter, datedelta, merge_refs)


def WeeklyWisdom(year, day_of_week):  # Weekly Wisdom
    # Solomon's Proverbial wisdom, the wisdom of the Preacher, and Wisdom and His Wife
    # ('Wisdom' being 'One Wiser than Solomon' )

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
        date = process_reading(date, book_abbr, chapter, 7)


def main():
    YEAR = 2020
    WeekdayPsalms(YEAR)
    WeekendPsalms(YEAR)
    WeekdayNT(YEAR)
    OTMain(YEAR)
    WeeklyWisdom(YEAR, "Sat")  # Saturdays with Solomon

    # for cal_date, full_refs in sorted(daily_readings.items()):
    #     print(cal_date, full_refs)  # Useful for debugging

    previous_month = ""
    for cal_date, full_refs in sorted(daily_readings.items()):
        month = cal_date[0:2]
        if month != previous_month:  # Month changed
            print(f"\n\t{calendar.month_name[int(month)]} 2020\n")
            previous_month = month
        print(cal_date[3:] + ":", ", ".join(full_refs))
        # 29 Tue: Psa 150, Rev 22, Mal 3-4


if __name__ == "__main__":
    main()
