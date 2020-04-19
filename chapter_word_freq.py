"""
Calculates the relative frequencies of each of the words in each chapter.
compared to its frequency in the entire Bible
"""

import csv
import json
import os

from lib.get_bible_metadata import get_word_frequency, get_book_nums

from chapter_word_freq_html import write_html_file

bible_metadata_folder = os.path.join(os.getcwd(), "BibleMetaData")


def print_word_info(word, values):

    (times_in_chapter, times_in_bible, weighted_freq) = values
    print(
        f"{word}: chapter: {times_in_chapter}, Bible: {times_in_bible}, weighted: {weighted_freq}"
    )
    # chapter: How many times this word is in the chapter
    # Bible: How many times this word is in the Bible
    # weighted: Weighted relative frequency of this word in the chapter,
    #           compared to its frequency in the entire Bible


def desc_value2_asc_key(element):

    """
    The weighted relative frequency of both "composition" and "atonements" in Exodus 30 is 815.1164948453609, because:
        2 out of 2 of the Bible's occurrences of "composition" are in this chapter
        1 out of 1 of the Bible's occurrences of "atonements" are in this chapter
    Of those, weight "composition" more highly (by giving it a more negative) sort key, so that it will be listed
    earlier in the .csv file.

    The sort_key calculations for the 2 corresponding rows of file "Exo 030 word_freq_bible.csv" are:

        composition,2,2,815.1164948453609
            element == ["composition", [1,1,815.1164948453609]]
            -1 * element[1][2] == -815.1164948453609
            -1 * element[1][0] == -2
            element[0] == "composition"
            sort_key == (-815.1164948453609, -2, "composition")
        atonements,1,1,815.1164948453609
            element == ["atonements", [1,1,815.1164948453609]]
            -1 * element[1][2] == -815.1164948453609
            -1 * element[1][0] == -1
            element[0] == "atonements"
            sort_key == (-815.1164948453609, -1, "atonements")
    """

    sort_key = (-1 * element[1][2], -1 * element[1][0], element[0])

    return sort_key


def handle_book_folder(
    chapter_words_folder, book_folder, previous_book_abbrev, book_abbrev
):

    if previous_book_abbrev != book_abbrev:
        book_nums = get_book_nums()
        book_num_name = f"{str(book_nums[book_abbrev]).zfill(2)}_{book_abbrev}"
        book_folder = os.path.join(chapter_words_folder, book_num_name)
        if not os.path.isdir(book_folder):
            os.mkdir(book_folder)

    return book_folder


def get_chapter_word_freqs(
    words_in_bible, words_in_chapter, word_frequencies, word_frequency
):

    chapter_word_freqs = {}
    for (chapter_frequency, words) in word_frequencies.items():
        if words != ["TOTAL WORDS"]:
            times_in_chapter = int(chapter_frequency)
            for word in words:
                times_in_bible = word_frequency[word]

                # TODO: Add this to .csv files
                ## Most natural way of stating algorithm
                # simple_relative_frequency = times_in_chapter / (
                #     times_in_bible / words_in_bible
                # )
                simple_relative_frequency = (
                    times_in_chapter * words_in_bible
                ) / times_in_bible

                ## Most natural way of stating algorithm
                # weighted_relative_frequency = (times_in_chapter / words_in_chapter) / (
                #     times_in_bible / words_in_bible
                # )
                # weighted_relative_frequency = (
                #     simple_relative_frequency / words_in_chapter
                # )

                values = [
                    int(chapter_frequency),
                    times_in_bible,
                    simple_relative_frequency / words_in_chapter,
                    simple_relative_frequency,
                ]
                chapter_word_freqs[word] = values

    return chapter_word_freqs


def get_relative_word_frequency(
    words_in_bible, words_in_chapter, word_frequencies, word_frequency
):

    relative_word_frequency = {}
    relative_word_frequency["TOTAL WORDS"] = [words_in_chapter]
    chapter_word_freqs = get_chapter_word_freqs(
        words_in_bible, words_in_chapter, word_frequencies, word_frequency
    )
    for chapter_word_freq, values in sorted(
        chapter_word_freqs.items(), key=desc_value2_asc_key
    ):
        relative_word_frequency[chapter_word_freq] = values

    return relative_word_frequency


def write_csv_file(words_in_bible, key, csv_fn, relative_word_frequency):

    with open(csv_fn, mode="w", newline="") as csv_file:
        # newline="" prevents blank lines from being added between rows
        writer = csv.writer(csv_file, delimiter=",", quotechar='"')
        writer.writerow(
            ["word", "numInChap", "numInKjv", "weightedRelFreq", "simpleRelFreq",]
        )
        #   Column header row

        for count, chapter_word_freq in enumerate(relative_word_frequency):
            values = relative_word_frequency[chapter_word_freq]
            if count:  # Data row
                writer.writerow(
                    [chapter_word_freq, values[0], values[1], values[2], values[3],]
                )
            else:  # Totals row
                writer.writerow(
                    [
                        f"TOTAL ({key})",
                        relative_word_frequency[chapter_word_freq][0],
                        words_in_bible,
                    ]
                )


def write_csv_and_html(
    words_in_bible, key, book_abbrev, book_folder, relative_word_frequency
):

    book_abbrev = key[0:3]
    chapter = key[4:].zfill(3)  # 0-pad for consistent cross-platform sorting

    csv_fn = os.path.join(book_folder, f"{book_abbrev} {chapter} word_freq.csv")
    write_csv_file(words_in_bible, key, csv_fn, relative_word_frequency)

    # In addition to the above .csv file, generate an .html file with sortable tables
    # Currently, that's done with method #1 below, but we may want to look at some of
    # other alternatives:
    #  *1. https://www.kryogenix.org/code/browser/sorttable/sorttable.js
    #   2. https://www.w3schools.com/howto/howto_js_sort_table.asp
    # **3. https://brython.info/gallery/sort_table.html
    # ***4. https://brython.info/gallery/sort_table_template.html
    #   5. https://stefanhoelzl.github.io/vue.py/examples/grid_component/
    #       source at
    #       https://github.com/stefanhoelzl/vue.py/blob/master/examples/grid_component/app.py
    #   6. https://anvil.works/docs/data-tables/data-tables-in-code#searching-querying-a-table

    html_fn = os.path.join(book_folder, f"{book_abbrev} {chapter} word_freq.html")
    write_html_file(words_in_bible, key, html_fn, relative_word_frequency)


def generate_word_freq_files():

    # TODO:
    # Refactor using a function which instead of calculating word frequencies in a chapter
    # relative to word frequencies in the Bible,
    # calculates word frequencies in a subunit, relative to word frequencies in a unit.
    # Such a function might be used for calculating (relative) word frequencies for the OT, NT,
    # individual book, daily readings, etc.

    words_in_bible = 790663
    word_frequency = get_word_frequency()
    chapters_relative_word_frequency = {}

    chapter_words_folder = os.path.join(bible_metadata_folder, "ChapterWords")
    if not os.path.isdir(chapter_words_folder):
        os.mkdir(chapter_words_folder)

    previous_book_abbrev = ""
    book_folder = ""
    read_fn = os.path.join(bible_metadata_folder, "word_frequency_lists_chapters.json")
    with open(read_fn, "r") as read_file:
        word_frequency_lists_chapters = json.load(read_file)
        for (key, word_frequencies) in word_frequency_lists_chapters.items():

            words_in_chapter = int(next(iter(word_frequencies)))
            relative_word_frequency = get_relative_word_frequency(
                words_in_bible, words_in_chapter, word_frequencies, word_frequency
            )
            chapters_relative_word_frequency[key] = relative_word_frequency

            book_abbrev = key[0:3]
            book_folder = handle_book_folder(
                chapter_words_folder, book_folder, previous_book_abbrev, book_abbrev
            )
            write_csv_and_html(
                words_in_bible, key, book_abbrev, book_folder, relative_word_frequency
            )
            previous_book_abbrev = book_abbrev

    with open(
        r"BibleMetaData\chapters_relative_word_frequency.json", "w"
    ) as write_file:
        json.dump(chapters_relative_word_frequency, write_file, indent=4)


def main():
    generate_word_freq_files()


if __name__ == "__main__":
    main()
