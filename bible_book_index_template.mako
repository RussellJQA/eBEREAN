## bible_book_index.mako
<%inherit file="base.mako"/>

    <main id='main_content' role='main' tabindex='-1'>
        % for chapter in range (1, chapters_in_book+1):
        <a href='${book_abbrev}${str(chapter).zfill(3)}_word_freq.html'>${book_abbrev}${str(chapter).zfill(3)} Word Frequencies</a><br>
        % endfor
    </main>
