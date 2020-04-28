import json
import os

bible_metadata_folder = os.path.join(os.getcwd(), "BibleMetaData")


def get_book_nums():
    read_fn = os.path.join(bible_metadata_folder, "book_numbers.json")
    with open(read_fn, "r") as read_file:
        book_nums = json.load(read_file)
        return book_nums


def get_verse_counts():
    read_fn = os.path.join(bible_metadata_folder, "verse_counts_by_chapter.json")
    with open(read_fn, "r") as read_file:
        verse_counts = json.load(read_file)
        return verse_counts
