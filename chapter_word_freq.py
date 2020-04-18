"""
Calculates the relative frequency of each of the words in each chapter.
compared to its frequency in the entire Bible
"""

import csv
import json
import os

from lib.get_bible_metadata import get_word_frequency, get_book_nums, get_verse_counts

bible_metadata_folder = os.path.join(os.getcwd(), "BibleMetaData")


def print_word_info(word, values):

    (chap_freq, word_freq, rel_freq) = values
    print(f"{word}: chapter: {chap_freq}, Bible: {word_freq}, relative: {rel_freq}")
    # chapter: How many times this word is in the chapter
    # Bible: How many times this word is in the Bible
    # relative: Relative frequency of this word in the chapter,
    #           compared to its frequency in the entire Bible


def desc_value2_asc_key(element):

    """
    The simple relative frequency of both "composition" and "atonements" in Exodus 30 is 815.1164948453609, because:
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


def main():

    overall_frequency = 790663
    word_frequency = get_word_frequency()
    chapters_relative_word_frequency = {}
    book_nums = get_book_nums()
    verse_counts = get_verse_counts()

    chapter_words_folder = os.path.join(bible_metadata_folder, "ChapterWords")
    if not os.path.isdir(chapter_words_folder):
        os.mkdir(chapter_words_folder)

    previous_book_abbrev = ""
    book_folder = ""
    read_fn = os.path.join(bible_metadata_folder, "word_frequency_lists_chapters.json")
    with open(read_fn, "r") as read_file:
        word_frequency_lists_chapters = json.load(read_file)
        for (key, word_frequencies) in word_frequency_lists_chapters.items():
            book_abbrev = key[0:3]
            book_num_name = f"{str(book_nums[book_abbrev]).zfill(2)}_{book_abbrev}"
            if previous_book_abbrev != book_abbrev:
                book_folder = os.path.join(chapter_words_folder, book_num_name)
                if not os.path.isdir(book_folder):
                    os.mkdir(book_folder)
            chapter_words = {}
            words_in_chapter = int(next(iter(word_frequencies)))
            chapter = key[4:].zfill(3)  # 0-pad for consistent cross-platform sorting
            csv_fn = os.path.join(book_folder, f"{book_abbrev} {chapter} word_freq.csv")

            # TODO: In addition to .csv files, generate .html files with sortable
            #       tables, based on 1 or more of the following:
            #  *1. https://www.kryogenix.org/code/browser/sorttable/sorttable.js
            #       See Gen 001 word_freq_bible.html in my Python Playground > Bible folder.
            #   2. https://www.w3schools.com/howto/howto_js_sort_table.asp
            # **3. https://brython.info/gallery/sort_table.html
            # ***4. https://brython.info/gallery/sort_table_template.html
            #   5. https://stefanhoelzl.github.io/vue.py/examples/grid_component/
            #       source at
            #       https://github.com/stefanhoelzl/vue.py/blob/master/examples/grid_component/app.py
            #   5. https://anvil.works/docs/data-tables/data-tables-in-code#searching-querying-a-table

            # TODO: Have 2 different relative frequency columns:
            #       1. simple relative frequency: Calculated from numInChap and numInKjv only
            #       2. weighted relative frequency: Take into account the total number of words in the chapter
            #           A word which is 1 time in a chapter of 100 words
            #           should have a greater relative frequency than a word
            #           which is 1 time in a chapter of 200 words.

            with open(csv_fn, mode="w", newline="") as csv_file:
                # newline="" prevents blank lines from being added between rows
                writer = csv.writer(csv_file, delimiter=",", quotechar='"')
                writer.writerow(["word", "numInChap", "numInKjv", "relativeFreq"])
                #   Column header row
                words_tot_hdr = f"TOTAL ({key})"
                num_verses = f"{verse_counts[key]} verses"
                #   The number of verses in the chapter (with " verses" for context)
                #   as in "176 verses" for Psalm 119.
                row = [words_tot_hdr, words_in_chapter, overall_frequency, num_verses]
                #   Totals row: I gave the row a final value to allow GitHub to
                #     "make this file beautiful and searchable"
                #     (to display it as a table, and allow it to be searchable).
                writer.writerow(row)
                for (chapter_frequency, words) in word_frequencies.items():
                    if words != ["TOTAL WORDS"]:
                        chap_freq = int(chapter_frequency)
                        for word in words:
                            word_freq = word_frequency[word]
                            relative_frequency = (chap_freq / words_in_chapter) * (
                                overall_frequency / word_freq
                            )
                            values = [
                                int(chapter_frequency),
                                word_freq,
                                relative_frequency,
                            ]
                            chapter_words[word] = values
                relative_word_frequency = {}
                relative_word_frequency["TOTAL WORDS"] = [words_in_chapter]
                for chapter_word, values in sorted(
                    chapter_words.items(), key=desc_value2_asc_key
                ):
                    relative_word_frequency[chapter_word] = values
                    writer.writerow([chapter_word, values[0], values[1], values[2]])
                chapters_relative_word_frequency[key] = relative_word_frequency

    with open(
        r"BibleMetaData\chapters_relative_word_frequency.json", "w"
    ) as write_file:
        json.dump(chapters_relative_word_frequency, write_file, indent=4)


if __name__ == "__main__":
    main()
