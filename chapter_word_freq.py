"""
Calculates the relative frequency of each of the words in each chapter.
compared to its frequency in the entire Bible
"""

import csv
import json
import os

bible_metadata_folder = os.path.join(os.getcwd(), "BibleMetaData")


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

    read_fn = os.path.join(bible_metadata_folder, "word_frequency_lists_chapters.json")
    with open(read_fn, "r") as read_file:
        word_frequency_lists_chapters = json.load(read_file)
        for (key, word_frequencies) in word_frequency_lists_chapters.items():
            chapter_words = {}
            words_in_chapter = int(next(iter(word_frequencies)))
            csv_fn = os.path.join(chapter_words_folder, key + " word_freq.csv")
            with open(csv_fn, mode="w") as csv_file:
                writer = csv.writer(csv_file, delimiter=",", quotechar='"')
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
                    row = [chapter_word, values[0], values[1], values[2]]
                    writer.writerow(row)
                chapters_relative_word_frequency[key] = relative_word_frequency

    with open(
        r"BibleMetaData\chapters_relative_word_frequency.json", "w"
    ) as write_file:
        json.dump(chapters_relative_word_frequency, write_file, indent=4)


if __name__ == "__main__":
    main()

