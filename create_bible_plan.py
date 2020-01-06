import calendar
import datetime
import json
import os

from create_bible_plan_playlists import create_bible_plan_playlists


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


def make_plan_folder(plan):
    if not os.path.isdir(plan):
        os.mkdir(plan)


def create_plan_with_playlists(plan, daily_readings):
    make_plan_folder(plan)
    previous_month = ""
    with open(plan + "/daily_readings.txt", "w") as readings_file:
        for (cal_date, full_refs) in sorted(daily_readings.items()):
            # items() returns a list of (key, value) tuples
            previous_month = print_daily_reading(
                plan, cal_date, previous_month, full_refs, readings_file
            )
            create_bible_plan_playlists(plan, cal_date, full_refs)


def print_daily_reading(plan, cal_date, previous_month, full_refs, readings_file):
    month = cal_date[0:2]
    if month != previous_month:  # Month changed
        month_header = f"\n\t{calendar.month_name[int(month)]} 2020\n"
        print(month_header)
        readings_file.write(f"{month_header}\n")
        previous_month = month

    daily_reading = "□ " + cal_date[3:] + ": " + ", ".join(full_refs)
    # □ 28 Mon: Psa 149:6-9, Rev 19, Zec 11-12
    print(daily_reading)

    # readings_file.write(f"{daily_reading}\n")
    # TOD: Eliminate the following error, resulting from the above line of code
    """
    UnicodeEncodeError: 'charmap' codec can't encode character '\u25a1' in position 0: character maps to <undefined>
    """
    readings_file.write(f"{daily_reading[2:]}\n")

    if cal_date[6:9] == "Sat":
        horizontal_rule = "------------------------------------------------------------"
        print(horizontal_rule)
        readings_file.write(f"{horizontal_rule}\n")

    return previous_month


def process_reading(
    daily_readings, date, book_abbr, reference, datedelta, merge_refs=False
):
    cal_date = date.strftime("%m/%d %a")
    full_ref = book_abbr + " " + reference

    def do_merge_refs():
        last_full_ref = daily_readings[cal_date][-1]
        last_book_abbr = last_full_ref[0 : last_full_ref.find(" ")]

        if last_book_abbr == book_abbr:

            with open("verse_counts_by_chapter.json", "r") as read_file:
                verse_counts_by_chapter = json.load(read_file)
                # print(verse_counts_by_chapter)

                daily_readings[cal_date][-1] += "-" + reference
                # Concatenate new reference to old reference, with a dash separating
                # TODO: Need to update this to properly merge OT split chapter refs:
                #   Num 6-7:1-47        => Num 6-7:47   (3/2)
                #   Num 7:48-89-8       => Num 7:48-89;8 {better: Num 7:48-8:26} (3/3)
                #   1Ch 6:1-48-6:49-81  => 1Ch 6:1-81 {better: just 1Ch 6}  {6/21}
                #   Ezr 2:1-36-2:37-70  => Ezr 2:1-70 {better: just Ezr 2}  {7/22}
                #   Neh 7:1-38-7:39-73  => Neh 7:1-73 {better: just Neh 7}  {7/30}
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

    return (daily_readings, (date + datetime.timedelta(days=datedelta)))
