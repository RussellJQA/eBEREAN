"""
Calculates the relative frequency of each of the words in each chapter.
compared to its frequency in the entire Bible
"""

import csv
import json
import os

bible_metadata_folder = os.path.join(os.getcwd(), "BibleMetaData")


def get_book_num(book_abrev):
    read_fn = os.path.join(bible_metadata_folder, "book_numbers.json")
    with open(read_fn, "r") as read_file:
        book_nums = json.load(read_file)
        return book_nums[book_abrev]


def get_word_frequency():
    read_fn = os.path.join(bible_metadata_folder, "word_frequency.json")
    with open(read_fn, "r") as read_file:
        word_frequency = json.load(read_file)
        return word_frequency


def print_word_info(word, values):
    (chap_freq, word_freq, rel_freq) = values
    print(f"{word}: chapter: {chap_freq}, Bible: {word_freq}, relative: {rel_freq}")
    # chapter: How many times this word is in the chapter
    # Bible: How many times this word is in the Bible
    # relative: Relative frequency of this word in the chapter,
    #           compared to its frequency in the entire Bible


def desc_value2_asc_key(element):
    sort_key = (-1 * element[1][2], element[0])
    return sort_key


def main():
    overall_frequency = 790663
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
            book_abbrev = key[0:3]
            book_num_name = f"{str(get_book_num(book_abbrev)).zfill(2)}_{book_abbrev}"
            if previous_book_abbrev != book_abbrev:
                book_folder = os.path.join(chapter_words_folder, book_num_name)
                if not os.path.isdir(book_folder):
                    os.mkdir(book_folder)
            chapter_words = {}
            words_in_chapter = int(next(iter(word_frequencies)))
            csv_fn = os.path.join(book_folder, f"{key} word_freq.csv")

            with open(csv_fn, mode="w", newline="") as csv_file:
                # newline="" prevents blank lines from being added between rows
                writer = csv.writer(csv_file, delimiter=",", quotechar='"')
                writer.writerow(["word", "numInChap", "numInKjv", "relativeFreq"])
                #   Column header row
                words_tot_hdr = f"TOTAL ({key})"
                writer.writerow([words_tot_hdr, words_in_chapter, overall_frequency, 0])
                #   Totals row (The row's final value was added to allow Github to
                #     "make this file beautiful and searchable"
                #     (to display it as a table, and allow it to be searchable).)
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

