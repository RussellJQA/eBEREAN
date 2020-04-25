from datetime import date

# pip-installed
from mako.template import Template

raw_template = Template(filename="bible_chapter_template.mako")

# Data which varies between Bible chapters
book_abbrev = "Gen"
chapter = "1"
words_in_chapter = "797"
rows = [["whales", "1", "1", "992.0", "790,663"],
        ["yielding", "5", "7", "708.6", "564,759"]]

# Data which is the same for each Bible chapter
description = "eBEREAN: electronic Bible Exploration REsources and ANalysis."
datestamp = date.today().strftime("%Y-%m-%d")
year = datestamp[0:4]
author = "Russell Johnson"
site = "RussellJ.heliohost.org"
title_h1 = f"{book_abbrev} {chapter}: KJV Chapter Word Frequencies"
og_site_name = "RussellJ"
words_in_bible = "790,663"

filled_in_template = raw_template.render(
    description=description,
    datestamp=datestamp,
    author=author,
    site=site,
    year=year,
    og_site_name=og_site_name,
    title_h1=title_h1,
    words_in_bible=words_in_bible,
    book_abbrev=book_abbrev,
    chapter=chapter,
    words_in_chapter=words_in_chapter,
    rows=rows,
)

html_fn = "Gen001_word_freq.html"
with open(html_fn, "w", newline="") as write_file:
    write_file.write(filled_in_template)
