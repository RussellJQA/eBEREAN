# Chapter files extracted from https://ebible.org/Scriptures/eng-kjv_readaloud.zip
# (linked to at https://ebible.org/kjv/)

# Above link and the following copyright information are from:
#   https://ebible.org/find/show.php?id=eng-kjv
"""

King James Version + Apocrypha
The King James Version or Authorized Version of the Holy Bible, using the standardized text of 1769, with Apocrypha/Deuterocanon
Public Domain
Language: English
Dialect: archaic British

Letters patent issued by King James with no expiration date means that to print this translation in the United Kingdom or import printed copies into the UK, you need permission. Currently, the Cambridge University Press, the Oxford University Press, and Collins have the exclusive right to print this Bible translation in the UK. This royal decree has no effect outside of the UK, where this work is firmly in the Public Domain. Please see http://www.cambridge.org/about-us/who-we-are/queens-printers-patent and https://en.wikipedia.org/wiki/King_James_Version#Copyright_status for more information. This free text of the King James Version of the Holy Bible is brought to you courtesy of the Crosswire Bible Society and eBible.org.


2018-08-27

"""

import glob
import json
import os.path
import re


def key_value(element):
    sort_key = (element[0], element[1])
    return sort_key


def desc_value_asc_key(element):
    sort_key = (-1 * element[1], element[0])
    return sort_key


def build_frequency_lists(frequency):
    total_words = 0  # The final value of total_words is 790,663
    words_with_this_frequency = []
    frequency_lists = {}
    prev_occurrences = 0
    occurrences = 0
    for element in sorted(frequency.items(), key=desc_value_asc_key):
        # Split into lists of words for each frequency:
        word = element[0]
        occurrences = element[1]  # For "the", occurrences is 64016
        total_words += occurrences
        if prev_occurrences and occurrences != prev_occurrences:
            frequency_lists[prev_occurrences] = words_with_this_frequency[:]
            words_with_this_frequency.clear()
        words_with_this_frequency.append(word)
        prev_occurrences = occurrences
    frequency_lists[occurrences] = words_with_this_frequency[:]
    frequency_lists = {total_words: ["TOTAL WORDS"], **frequency_lists}

    total_words2 = 0  # Essentially, recalc total_words a 2nd way, for comparison.
    for key, value in sorted(frequency_lists.items(), reverse=True):
        if value != ["TOTAL WORDS"]:
            total_words2 += int(key) * len(value)
            # Increment by number of occurrences * number of words with that number
    if total_words != total_words2:
        print(f"total_words ({total_words}) != to total_words2 ({total_words2})")

    return frequency_lists


def build_frequency_lists(frequency):
    total_words = 0  # The final value of total_words is 790,663
    words_with_this_frequency = []
    frequency_lists = {}
    prev_occurrences = 0
    occurrences = 0
    for element in sorted(frequency.items(), key=desc_value_asc_key):
        # Split into lists of words for each frequency:
        word = element[0]
        occurrences = element[1]  # For "the", occurrences is 64016
        total_words += occurrences
        if prev_occurrences and occurrences != prev_occurrences:
            frequency_lists[prev_occurrences] = words_with_this_frequency[:]
            words_with_this_frequency.clear()
        words_with_this_frequency.append(word)
        prev_occurrences = occurrences
    frequency_lists[occurrences] = words_with_this_frequency[:]
    frequency_lists = {total_words: ["TOTAL WORDS"], **frequency_lists}

    total_words2 = 0  # Essentially, recalc total_words a 2nd way, for comparison.
    for key, value in sorted(frequency_lists.items(), reverse=True):
        if value != ["TOTAL WORDS"]:
            total_words2 += int(key) * len(value)
            # Increment by number of occurrences * number of words with that number
    if total_words != total_words2:
        print(f"total_words ({total_words}) != to total_words2 ({total_words2})")

    return frequency_lists


def write_word_frequency_files(word_frequency, word_frequency_lists_chapters):

    # Write dict of KJV words, each paired (in a list) with its # of occurrences
    # {["a", 8282], ["aaron", 350], ["aaronites", 2], ... ["zuzims", 1]}
    word_frequency_sorted = {}
    for key, value in sorted(word_frequency.items()):
        word_frequency_sorted[key] = value
    with open(r"BibleMetaData\word_frequency.json", "w") as write_file:
        json.dump(word_frequency_sorted, write_file)

    word_frequency_lists = build_frequency_lists(word_frequency)
    with open(r"BibleMetaData\word_frequency_lists.json", "w") as write_file:
        json.dump(word_frequency_lists, write_file, indent=4)

    with open(r"BibleMetaData\word_frequency_lists_chapters.json", "w") as write_file:
        json.dump(word_frequency_lists_chapters, write_file, indent=4)


def main():
    book_abbrevs = {}
    verse_counts_by_chapter = {}  # dict of verse counts, indexed by chapter
    # e.g., dict["Gen 1"]=31
    verse_counts_by_count = {}  # dict of full_refs, indexed by verse counts
    verse_counts_by_desc_count = {}  # above dict, sorted by decreasing verse count
    word_frequency = {}
    word_frequency_lists_chapters = {}
    word_frequency_this_chapter = {}

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_files = os.path.join(script_dir, "downloads", "kjv_chapter_files")
    kjv_chapter_files = sorted(glob.glob(os.path.join(source_files, "*.txt")))
    # sorted() because glob() may return the list in an arbitrary order

    chapter_count = 0
    for chapter_file in kjv_chapter_files:
        chapter_count += 1
        read_file = open(chapter_file, "r", encoding="utf-8")
        lines = read_file.readlines()
        # There's no need to exclude the blank line at the end of chapter files,
        # since readlines() already seems to ignore it.

        book_number_name_chapter = os.path.basename(chapter_file)[9:-9]
        # basename is, for example, eng-kjv_002_GEN_01_read.txt
        book_number = int(book_number_name_chapter[0:2]) - 1
        # Sets the book number for 'eng-kjv_002_GEN_01_read.txt' to 1
        # Sets the book number for 'eng-kjv_070_MAT_01_read.txt' to 69
        if book_number >= 40:
            book_number -= 29
        # Sets the book number for 'eng-kjv_070_MAT_01_read.txt' to (70 - 1) - 29 = 40
        book_abbr = book_number_name_chapter[3:6].title()  # Gen, Exo, ..., Rev
        if book_abbr not in book_abbrevs:
            full_book_name = lines[0][1:]  # Strip unwanted initial Unicode character
            book_abbrevs[book_abbr] = full_book_name
        chapter_number = book_number_name_chapter[7:10].lstrip("0").rstrip("_")
        # Filenames normally contain 2-digit chapter numbers, but have 3 for Psalms
        # Remove leading '0's (as from '01' and '001') and trailing '_'s (as from '01_')
        # print(f'Book number: {book_number}, abbr: {book_abbr}, chapter: {chapter_number}')

        # Calculate verse counts
        full_ref = book_abbr + " " + chapter_number
        verse_count = len(lines) - 2  # Exclude lines[0] and lines [1]
        verse_counts_by_chapter[full_ref] = verse_count
        if verse_count in verse_counts_by_count:
            verse_counts_by_count[verse_count].append(full_ref)
        else:
            verse_counts_by_count[verse_count] = [full_ref]

        # TODO: Put this into a function
        # Calculate word frequencies
        frequency_this_chapter = {}
        for line in lines[2:]:
            line = re.sub("[¶’]\S*", "", line).strip()
            # Eliminate paragraph markers, possessives, and leading/trailing blanks
            words = re.sub("[^a-z\- ]+", "", line, flags=re.IGNORECASE)
            for word in words.split():
                word_lower = word.lower()  # TODO: Exclude "LORD" (, etc.?)

                if word_lower in word_frequency:
                    word_frequency[word_lower] += 1
                else:
                    word_frequency[word_lower] = 1
                if word_lower in frequency_this_chapter:
                    frequency_this_chapter[word_lower] += 1
                else:
                    frequency_this_chapter[word_lower] = 1

        frequency_lists_this_chapter = build_frequency_lists(frequency_this_chapter)
        word_frequency_lists_chapters[full_ref] = frequency_lists_this_chapter

    write_word_frequency_files(word_frequency, word_frequency_lists_chapters)

    with open(r"BibleMetaData\book_abbreviations.json", "w") as write_file:
        json.dump(book_abbrevs, write_file, indent=4)

    with open(r"BibleMetaData\verse_counts_by_chapter.json", "w") as write_file:
        json.dump(verse_counts_by_chapter, write_file, indent=4)

    for verse_count, full_refs in sorted(verse_counts_by_count.items(), reverse=True):
        verse_counts_by_desc_count[verse_count] = full_refs
    with open(r"BibleMetaData\verse_counts_by_desc_count.json", "w") as write_file:
        json.dump(verse_counts_by_desc_count, write_file, indent=4)


if __name__ == "__main__":
    main()
