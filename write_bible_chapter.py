from datetime import date

# pip-installed
from mako.template import Template
from mako.lookup import TemplateLookup

template_lookup = TemplateLookup(["lib"])
raw_template = Template(filename="bible_chapter_template.mako", lookup=template_lookup)

# Data which varies between Bible chapters
book_abbrev = "Gen"
chapter = "1"
words_in_chapter = "797"
rows = [
    ["whales", "1", "1", "992.0", "790,663"],
    ["yielding", "5", "7", "708.6", "564,759"],
]

# Data which is the same for each Bible chapter
description = "eBEREAN: electronic Bible Exploration REsources and ANalysis."
datestamp = date.today().strftime("%Y-%m-%d")
year = datestamp[0:4]
author = "Russell Johnson"
site = "RussellJ.heliohost.org"
title_h1 = f"{book_abbrev} {chapter}: KJV Chapter Word Frequencies"
og_site_name = "RussellJ"
words_in_bible = "790,663"

base_template_args = {
    "description": description,
    "datestamp": datestamp,
    "author": author,
    "site": site,
    "year": year,
    "og_site_name": og_site_name,
    "title_h1": title_h1,
}

new_template_args = {
    "book_abbrev": book_abbrev,
    "chapters_in_book": 50,
    "chapter": chapter,
    "words_in_bible": words_in_bible,
    "words_in_chapter": words_in_chapter,
    "rows": rows,
}

filled_in_template_args = {**base_template_args, ** new_template_args}
# In Python 3.9, PEP 584 will let you add 2 dicts using | or |=
filled_in_template = raw_template.render(**filled_in_template_args)

html_fn = "Gen001_word_freq.html"
with open(html_fn, "w", newline="") as write_file:
    write_file.write(filled_in_template)
