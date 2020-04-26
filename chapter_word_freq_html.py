from datetime import date

# pip-installed
from mako.template import Template

# TODO: Add a master index page
# TODO: Add favicon

meta_name_mako = Template(
    """<meta charset="UTF-8">
    <meta name="description" content="${description}">
    <meta name="date" content="${datestamp}">
    <meta name="last-modified" content="${datestamp}">
    <meta name="language" content="english">
    <meta name="author" content="${author} (${site})">
    <meta name="copyright" content="${year} ${author}. All rights reserved.">
    <meta name="generator" content="HTML">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">"""
)

head = Template(
    """

<head>
    ${meta_names}
    <meta property="og:site_name" content="${og_site_name}">
    <title>${title}</title>
    <!-- The table styling in this style tag is from https://www.w3schools.com/html/html_tables.asp -->
    <style>
        table,
        th,
        td {
            border: 1px solid black;
        }

        th,
        td {
            padding: 15px;
        }

        .integer {
            text-align: right;
        }

        footer {
            text-align: center
        }
    </style>
</head>

"""
)

header = Template(
    """
    <header role="banner">
        <h1>${h1}</h1>
    </header>
"""
)

main_start = Template(
    """
    <main id="main_content" role="main" tabindex="-1">
        <h2>${h2}</h2>
        <a download="${fn}" href="${fn}" target="_blank">Download ${fn}</a><br>
        <p>
            The columns in the sortable table below are:
            <ul>
                <li>Word:		A word which occurs in this chapter of the KJV Bible</li>
                <li>In chapter:	The number of occurrences of that word in this chapter of the KJV</li>
                <li>In KJV:		The number of occurrences of that word in the entire KJV</li>
                <li>Weighted:	The weighted relative frequency of that word in this chapter of the KJV</li>
                <li>Simple:		The simple relative frequency of that word in this chapter of the KJV</li>
            </ul>
            (See TBD for further explanation of both types of relative frequency.)
        </p>

"""
)

table_start = """
        <!-- Table sorting uses the following script, as explained at
        https://stackoverflow.com/questions/10683712/html-table-sort/51648529 -->
        <script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>

        <!-- Prototype table generated using http://convertcsv.com/csv-to-html.htm -->

        <!-- I removed the Bootstrap classes and align attributes from the generated table. -->
        <!-- <table class="table table-bordered table-hover table-condensed"> -->
        <table class="sortable">
            <thead>
                <tr>
                    <th title="Field #1">Word</th>
                    <th title="Field #2">In chapter</th>
                    <th title="Field #3">In KJV</th>
                    <th title="Field #4">Weighted Relative Frequency</th>
                    <th title="Field #4">Simple Relative Frequency</th>
                </tr>
            </thead>
            <tbody>"""

table_row = Template(
    """
                <tr>
                    <td>${word}</td>
                    <td class="integer">${numInChap}</td>
                    <td class="integer">${numInKjv}</td>
                    <td>${weightedRelFreq}</td>
                    <td>${simpleRelFreq}</td>
                </tr>"""
)

table_end = """
            </tbody>
        </table>
"""

footer = Template(
    """
    <footer role="contentinfo"><p>Copyright &copy; ${year} by ${author}</p></footer>
"""
)


def get_main_tag(words_in_bible, key, relative_word_frequency):

    main_tag = ""

    words_in_chapter = "{:,}".format(relative_word_frequency["TOTAL WORDS"][0])
    words_in_bible_formatted = "{:,}".format(words_in_bible)
    #   Include thousands separators
    book_and_chapter = f"{key[0:3]}{str(key[4:]).zfill(3)}"
    main_tag += main_start.render(
        h2=f"{words_in_chapter} word occurrences in {key} in the KJV ({words_in_bible_formatted} word occurrences in the entire KJV):",
        fn=f"{book_and_chapter}_word_freq.csv",
    )

    main_tag += table_start
    for count, chapter_word_freq_key in enumerate(relative_word_frequency):
        if count:  # Table row data
            values = relative_word_frequency[chapter_word_freq_key]
            # Include thousands separators, where needed
            main_tag += table_row.render(
                word=chapter_word_freq_key,
                numInChap=values[0],
                numInKjv=("{:,}".format(values[1])),
                weightedRelFreq=values[2],
                simpleRelFreq=("{:,}".format(values[3])),
            )
    main_tag += table_end

    main_tag += "    </main>"  # Closing <main> tag

    return main_tag


def write_html_file(html_fn, title_h1, main_tag):

    with open(html_fn, "w") as write_file:

        write_file.write("<!doctype html>\n")
        write_file.write("<html lang='en'>")

        datestamp = date.today().strftime("%Y-%m-%d")
        year = datestamp[0:4]
        author = "Russell Johnson"

        meta_tags = meta_name_mako.render(
            description="eBEREAN: electronic Bible Exploration REsources and ANalysis.",
            datestamp=datestamp,
            site="RussellJ.heliohost.org",
            author=author,
            year=year,
        )

        write_file.write(
            head.render(meta_names=meta_tags, og_site_name="RussellJ", title=title_h1)
        )

        write_file.write("<body>")  # Write start of <body> tag
        write_file.write(header.render(h1=title_h1))
        write_file.write(main_tag)  #   Write <main> tag
        write_file.write(footer.render(year=year, author=author))
        write_file.write("</body>\n\n")  # Write end of <body> tag

        write_file.write("</html>")


def main():
    pass


if __name__ == "__main__":
    main()
