import csv
import json
from pathlib import Path

json_fn = Path("BibleMetaData", "bible_books.json")
csv_fn = Path("BibleMetaData", "bible_book_info.csv")

with open(json_fn, "r") as json_file, open(csv_fn, "w") as csv_file:
    
    csv_file.write("Book,Abbreviation,Chapters\n")

    bible_book_info = json.load(json_file)
    for book, info in bible_book_info.items():
        book_abbr = info[0]
        chapter_count = info[1]
        csv_file.write(f"{book},{book_abbr},{chapter_count}\n")
