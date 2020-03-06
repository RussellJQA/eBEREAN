import calendar
import datetime
import json
import os
import re

from lib.get_bible_metadata import get_verse_counts

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


def create_plan_with_playlists(plan, daily_readings):
    previous_month = ""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    plan_folder = os.path.join(script_dir, "BiblePlanOutput", plan)
    if not os.path.isdir(plan_folder):
        os.mkdir(plan_folder)
    os.chdir(plan_folder)
    readings_fn = os.path.join(plan_folder, "daily_readings.txt")
    with open(readings_fn, "w", encoding="utf-8") as readings_file:
        # 'utf-8' allows including Unicode "□" (U+25A1: White Square) character
        for (cal_date, full_refs) in sorted(daily_readings.items()):
            # items() returns a list of (key, value) tuples
            previous_month = print_daily_reading(
                plan, cal_date, previous_month, full_refs, readings_file
            )
            create_bible_plan_playlists(plan, cal_date, full_refs)


def print_daily_reading(plan, cal_date, previous_month, full_refs, readings_file):

    # TODO: Refactor to add additional output formats, such as CSV or TSV; HTML; and RTF

    month = cal_date[0:2]
    if month != previous_month:  # Month changed
        month_header = f"\n\t{calendar.month_name[int(month)]} 2020\n"
        print(month_header)
        readings_file.write(f"{month_header}\n")
        previous_month = month

    daily_reading = "□ " + cal_date[3:] + ": " + ", ".join(full_refs)
    # □ 28 Mon: Psa 149:6-9, Rev 19, Zec 11-12
    print(daily_reading)
    readings_file.write(f"{daily_reading}\n")

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

    def merge_2_refs(ref1, ref2):

        # Merge "Num 6" and (Num) "7:1-47" to "Num 6:1-7:47"   (3/2)
        pattern1 = r"([1-3A-Z][a-z][a-z] \d{1,3})"
        match1 = re.search(pattern1, ref1)
        pattern2 = r"(\d{1,3})(\:1\-)(\d{1,3})"
        match2 = re.search(pattern2, ref2)
        if match1 and match2:
            return f"{match1.group(1)}:1-{match2.group(1)}:{match2.group(3)}"

        else:
            # Merge "Num 7:48-89" and (Num) "8" to "Num 7:48-8:26"   (3/3)
            pattern1 = r"([1-3A-Z][a-z][a-z] )(\d{1,3}\:\d{1,3})(\-)(\d{1,3})"
            match1 = re.search(pattern1, ref1)
            pattern2 = r"(\d{1,3})"
            match2 = re.search(pattern2, ref2)
            if match1 and match2:
                book_with_space = match1.group(1)
                ref1_chapter = match1.group(2)
                ref2_chapter = match2.group(1)
                verse_counts = get_verse_counts()  # TODO: Avoid calling multiple times
                verses = verse_counts[f"{book_with_space}{ref2_chapter}"]
                return f"{book_with_space}{ref1_chapter}-{ref2_chapter}:{verses}"

            else:
                pattern = r"([1-3A-Z][a-z][a-z] )(\d{1,3})(\:)(\d{1,3})(\-)(\d{1,3}) ([1-3A-Z][a-z][a-z] )(\d{1,3})(\:)(\d{1,3})(\-)(\d{1,3})"
                match = re.search(pattern, f"{ref1} {ref2}")
                if (
                    match
                    and (match.group(1) == match.group(6))
                    and (match.group(2) == match.group(7))
                ):
                    book_with_space = match1.group(1)
                    ref1_chapter = match1.group(2)
                    ref2_chapter = match2.group(1)
                    return ref1 + "-" + ref2
                else:
                    return ref1 + "-" + ref2

        # TODO: Refactor above to properly merge other OT split chapter refs.
        # For now, just hand-tweak them in any output files

        # Step 1: Use additional regular expressions to match the following patterns:
        #   1Ch 6:1-48, 6:49-81  => 1Ch 6:1-81 {better: just 1Ch 6}  {6/21}
        #   Ezr 2:1-36, 2:37-70  => Ezr 2:1-70 {better: just Ezr 2}  {7/22}
        #   Neh 7:1-38, 7:39-73  => Neh 7:1-73 {better: just Neh 7}  {7/30}

        # Step 2: Further refactor to get the "better" representations,
        #   by looking up verse counts in verse_counts_by_chapter.json

    def do_merge_refs():
        last_full_ref = daily_readings[cal_date][-1]
        last_book_abbr = last_full_ref[0 : last_full_ref.find(" ")]
        # Concatenate new reference to old reference, with a dash separating

        if last_book_abbr == book_abbr:
            bible_metadata_folder = os.path.join(os.getcwd(), "BibleMetaData")
            read_fn = os.path.join(
                bible_metadata_folder, "verse_counts_by_chapter.json"
            )
            with open(read_fn, "r") as read_file:
                verse_counts_by_chapter = json.load(read_file)
                # print(verse_counts_by_chapter)

                daily_readings[cal_date][-1] = merge_2_refs(
                    daily_readings[cal_date][-1], reference
                )

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
