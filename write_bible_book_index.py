from datetime import date

# pip-installed
from mako.template import Template

raw_template = Template(filename="bible_book_index_template.mako")

# Data which varies between Bible books
book_abbrev = "Gen"
chapters_in_book = 50

# Data which is the same for each Bible book
description = "eBEREAN: electronic Bible Exploration REsources and ANalysis."
datestamp = date.today().strftime("%Y-%m-%d")
year = datestamp[0:4]
author = "Russell Johnson"
site = "RussellJ.heliohost.org"
title_h1 = f"{book_abbrev}: KJV Chapter Word Frequencies"
og_site_name = "RussellJ"

filled_in_template = raw_template.render(
    description=description,
    datestamp=datestamp,
    author=author,
    site=site,
    year=year,
    og_site_name=og_site_name,
    title_h1=title_h1,
    book_abbrev=book_abbrev,
    chapters_in_book=50
)

html_fn = "Gen_index.html"
with open(html_fn, "w", newline="") as write_file:
    write_file.write(filled_in_template)
