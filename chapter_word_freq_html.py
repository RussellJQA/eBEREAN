import string

ENDING = """
        </tbody>
    </table>
</body>

</html>
"""

beginning = string.Template(
    """<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$key - Word Frequencies</title>
    <h1>$key - Word Frequencies</h1>
    <h2>TOTAL (Gen 1),797,$words_in_bible</h2>
     <!-- The CSS in this style tag is from https://www.w3schools.com/html/html_tables.asp -->
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
    </style>
</head>

<body>
    <!-- Sorting uses the following script, as explained at
    https://stackoverflow.com/questions/10683712/html-table-sort/51648529 -->
    <script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>

    <!-- Prototype table generated using http://convertcsv.com/csv-to-html.htm -->

    <!-- I removed the Bootstrap classes from the generated table. -->
    <!-- <table class="table table-bordered table-hover table-condensed"> -->
    <table class="sortable">
        <thead>
            <tr>
                <th title="Field #1">word</th>
                <th title="Field #2">numInChap</th>
                <th title="Field #3">numInKjv</th>
                <th title="Field #4">weightedRelFreq</th>
                <th title="Field #4">simpleRelFreq</th>
            </tr>
        </thead>
        <tbody>"""
)

table_row = string.Template(
    """
            <tr>
                <td>$word</td>
                <td align='right'>$numInChap</td>
                <td align='right'>$numInKjv</td>
                <td>$weightedRelFreq</td>
                <td>$simpleRelFreq</td>
            </tr>"""
)


def write_html_file(words_in_bible, key, html_fn, relative_word_frequency):

    with open(html_fn, "w") as write_file:

        values = {
            "key": key,
            "words_in_bible": words_in_bible,
        }
        write_file.write(beginning.substitute(values))

        for count, chapter_word_freq in enumerate(relative_word_frequency):
            values = relative_word_frequency[chapter_word_freq]
            if count:  # Data row
                values = {
                    "word": chapter_word_freq,
                    "numInChap": values[0],
                    "numInKjv": values[1],
                    "weightedRelFreq": values[2],
                    "simpleRelFreq": values[3],
                }
                write_file.write(table_row.substitute(values))

        write_file.write(ENDING)


def main():
    pass


if __name__ == "__main__":
    main()
