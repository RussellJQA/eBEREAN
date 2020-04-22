import string

# TODO: Add an index page

BODY_ENDING = """
    </main>
    <footer class='page' role='contentinfo'><p>Copyright &copy; 2020 by Russell Johnson</p></footer>
</body>

"""

head = string.Template(
    """
<head>
    <meta charset="UTF-8">
    <meta name='description' content='eBEREAN: electronic Bible Exploration REsources and ANalysis.'> 
    <meta name='date' content='2020-04-20'> 
    <meta name='last-modified' content='2020-04-20'>     
    <meta name='language' content='english' >
    <meta name='author' content='Russell Johnson (RussellJ.heliohost.org)' >
    <meta name='copyright' content="2020 Russell Johnson. All rights reserved." >
    <meta name='generator' content="HTML">
    <meta property="og:site_name" content="RussellJ"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$title</title>
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
</head>"""
)

# TODO: Add favicon

body_start = string.Template(
    """
<body>
    <header class='page' role='banner'>
        <h1>$h1</h1>
    </header>
    <main id='main_content'  class='page' class='page' role='main' tabindex='-1'>
        <h2>$h2</h2>
        
        <p>
            The columns in the sortable table below are:
            <ul>
                <li>Word:		A word which occurs in this chapter of the KJV Bible</li>
                <li>In chapter:	The number of occurrences of that word in this chapter of the KJV</li>
                <li>In KJV:		The number of occurrences of that word in the entire KJV</li>
                <li>Weighted:	The weighted relative frequency of that word in this chapter of the KJV</li>
                <li>Simple:		The simple relative frequency of that word in this chapter of the KJV</li>
            </ul>
            (See TBD for an explanation of both types of relative frequency.)
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

table_row = string.Template(
    """
                <tr>
                    <td>$word</td>
                    <td class='integer'>$numInChap</td>
                    <td class='integer'>$numInKjv</td>
                    <td>$weightedRelFreq</td>
                    <td>$simpleRelFreq</td>
                </tr>"""
)

table_end = """
            </tbody>
        </table>"""


def write_html_file(words_in_bible, key, html_fn, relative_word_frequency):

    with open(html_fn, "w") as write_file:

        write_file.write("<!doctype html>")
        write_file.write("<html lang='en'>")

        # Write <head> tag

        values = {
            "title": f"{key}: KJV Chapter Word Frequencies",
        }
        write_file.write(head.substitute(values))

        # Write <body> tag

        for count, chapter_word_freq in enumerate(relative_word_frequency):
            values = relative_word_frequency[chapter_word_freq]
            if count:  # Table row data
                # Include thousands separators, where needed
                values = {
                    "word": chapter_word_freq,
                    "numInChap": values[0],
                    "numInKjv": ("{:,}".format(values[1])),
                    "weightedRelFreq": values[2],
                    "simpleRelFreq": ("{:,}".format(values[3])),
                }
                write_file.write(table_row.substitute(values))
            else:  # Start of <body> tag
                # Include thousands separators in the numbers below
                words_in_chapter = "{:,}".format(
                    relative_word_frequency[chapter_word_freq][0]
                )
                words_in_bible_formatted = "{:,}".format(words_in_bible)
                values = {
                    "h1": f"{key}: KJV Chapter Word Frequencies",
                    "h2": f"{words_in_chapter} word occurrences in {key} in the KJV ({words_in_bible_formatted} word occurrences in the entire KJV):",
                }
                write_file.write(body_start.substitute(values))
                write_file.write(table_start)

        write_file.write(table_end)
        write_file.write(BODY_ENDING)
        write_file.write("</html>")


def main():
    pass


if __name__ == "__main__":
    main()
