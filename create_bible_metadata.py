"""

King James Version + Apocrypha
The King James Version or Authorized Version of the Holy Bible, using the standardized text of 1769, with Apocrypha/Deuterocanon
Public Domain
Language: English
Dialect: archaic British

Letters patent issued by King James with no expiration date means that to print this translation in the United Kingdom or import printed copies into the UK,
you need permission.
Currently, the Cambridge University Press, the Oxford University Press, and Collins have the exclusive right to print this Bible
translation in the UK. This royal decree has no effect outside of the UK, where this work is firmly in the Public Domain.
Please see http://www.cambridge.org/about-us/who-we-are/queens-printers-patent and https://en.wikipedia.org/wiki/King_James_Version#Copyright_status
for more information.
This free text of the King James Version of the Holy Bible is brought to you courtesy of the Crosswire Bible Society and eBible.org.


2018-08-27

"""
# Chapter files extracted from https://ebible.org/Scriptures/eng-kjv_readaloud.zip
# (linked to at https://ebible.org/kjv/)

# Above link and the following copyright information are from:
#   https://ebible.org/find/show.php?id=eng-kjv

import glob
import json
import os.path


def calc_and_write_book_abbrevs():

    # TODO: Use VSCode autoDocstring extension to quickly generate
    #       docstring prototypes like the following, and complete them.
    """[summary]

    Arguments:
        element {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_files = os.path.join(script_dir, "downloads", "kjv_chapter_files")
    kjv_chapter_01_files = glob.glob(os.path.join(source_files, "*_01_read.txt"))
    #   List files for the 1st chapter of every Bible book except for Psalms
    kjv_chapter_01_files.extend(glob.glob(os.path.join(source_files, "*_001_read.txt")))
    #   Append name of the file for the 1st chapter of Psalms
    kjv_chapter_01_files.sort()

    book_abbrevs = {}
    for chapter_01 in kjv_chapter_01_files:
        with open(chapter_01, "r", encoding="utf-8") as read_file:
            book_abbr = os.path.basename(chapter_01)[12:15].title()  # Gen, Exo, ...
            # basename is, for example, eng-kjv_002_GEN_01_read.txt
            full_book_name = read_file.readline()[1:].strip().strip(".").title()
            # Strip unwanted initial Unicode character, etc.
            book_abbrevs[book_abbr] = full_book_name

    with open(r"BibleMetaData\book_abbreviations.json", "w") as write_file:
        json.dump(book_abbrevs, write_file, indent=4)

    return book_abbrevs


def calc_and_write_book_nums(book_abbrevs):

    book_nums = {}
    for book_num, abbrev in enumerate(book_abbrevs.keys(), start=1):
        book_nums[abbrev] = book_num
    with open(r"BibleMetaData\book_numbers.json", "w") as write_file:
        json.dump(book_nums, write_file, indent=4)


def calc_verse_data(chapter_file, lines):

    book_number_name_chapter = os.path.basename(chapter_file)[9:-9]
    # basename is, for example, eng-kjv_002_GEN_01_read.txt
    book_abbr = book_number_name_chapter[3:6].title()  # Gen, Exo, ..., Rev
    chapter_number = book_number_name_chapter[7:10].lstrip("0").rstrip("_")
    # Filenames normally contain 2-digit chapter numbers, but have 3 for Psalms
    # Remove leading '0's (as from '01' and '001') and trailing '_'s (as from '01_')

    # Calculate verse counts
    full_ref = book_abbr + " " + chapter_number
    verse_count = len(lines) - 2  # Exclude lines[0] and lines [1]
    return (full_ref, verse_count)


def calc_and_write_verse_counts_by_desc_count(verse_counts_by_chapter):

    with open(r"BibleMetaData\verse_counts_by_chapter.json", "w") as write_file:
        json.dump(verse_counts_by_chapter, write_file, indent=4)

    # Calculate verse_counts_by_count by summing from verse_counts_by_chapter
    verse_counts_by_count = {}  # dict of full_refs, indexed by verse counts
    for full_ref, verse_count in verse_counts_by_chapter.items():
        if verse_count in verse_counts_by_count:
            verse_counts_by_count[verse_count].append(full_ref)
        else:
            verse_counts_by_count[verse_count] = [full_ref]

    verse_counts_by_desc_count = {}
    #   verse_counts_by_count, sorted by decreasing verse count
    for verse_count, full_refs in sorted(verse_counts_by_count.items(), reverse=True):
        verse_counts_by_desc_count[verse_count] = full_refs
    with open(r"BibleMetaData\verse_counts_by_desc_count.json", "w") as write_file:
        json.dump(verse_counts_by_desc_count, write_file, indent=4)


def desc_value_asc_key(element):

    sort_key = (-1 * element[1], element[0])
    return sort_key


def main():

    book_abbrevs = calc_and_write_book_abbrevs()  # Calculate/write dict
    calc_and_write_book_nums(book_abbrevs)

    verse_counts_by_chapter = {}  # dict of verse counts, indexed by chapter
    #   e.g., verse_counts_by_chapter["Gen 1"]=31

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_files = os.path.join(script_dir, "downloads", "kjv_chapter_files")
    kjv_chapter_files = sorted(glob.glob(os.path.join(source_files, "*.txt")))
    # sorted() because glob() may return the list in an arbitrary order

    for chapter_file in kjv_chapter_files:
        read_file = open(chapter_file, "r", encoding="utf-8")
        lines = read_file.readlines()
        # There's no need to exclude the blank line at the end of chapter files,
        # since readlines() already seems to ignore it.

        (full_ref, verse_count) = calc_verse_data(chapter_file, lines)
        verse_counts_by_chapter[full_ref] = verse_count

    calc_and_write_verse_counts_by_desc_count(verse_counts_by_chapter)


if __name__ == "__main__":
    main()
