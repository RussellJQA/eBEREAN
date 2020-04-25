<!doctype html>
<html lang='en'>

<head>
    <meta charset="UTF-8">
    <meta name="description" content="${description}">
    <meta name="date" content="${datestamp}">
    <meta name="last-modified" content="${datestamp}">
    <meta name="language" content="english">
    <meta name="author" content="${author} (${site})">
    <meta name="copyright" content="${year} ${author}. All rights reserved.">
    <meta name="generator" content="HTML">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:site_name" content="${og_site_name}">
    <title>${title_h1}</title>
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

<body>
    <header class="page" role="banner">
        <h1>${title_h1}</h1>
    </header>
    <main id='main_content' class='page' class='page' role='main' tabindex='-1'>
        % for chapter in range (1, chapters_in_book+1):
        <a href='${book_abbrev}${str(chapter).zfill(3)}_word_freq.html'>${book_abbrev}${str(chapter).zfill(3)} Word Frequencies</a><br>
        % endfor
    </main>
    <footer class="page" role="contentinfo">
        <p>Copyright &copy; ${year} by ${author}</p>
    </footer>
</body>

</html>