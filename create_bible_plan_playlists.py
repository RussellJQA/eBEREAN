"""
Create an MP3 playlist for each day in the specified Bible reading plan.
"""

import re

from lib.bible_books import bible_books


def create_bible_plan_playlists(cal_date, full_refs, m3u_ext="m3u"):
    """
    An .m3u8 file is essentially the same as an .m3u file, but it's UTF-8 encoded.
    .m3u was chosen as the default extension since some platforms don't support .m3u8.
    """

    def get_book_chapter_verse(reference):

        book_abbr = reference[0:3]
        book_number_and_name = book_numbers_and_names[book_abbr]
        book_num = book_number_and_name[0:2]
        chapter_verse_ref = reference[4:].zfill(3 if book_num <= "39" else 2)
        return (book_abbr, book_number_and_name, book_num, chapter_verse_ref)

    mp3_path = "/storage/emulated/0/Music/Bible-Audio/"
    book_numbers_and_names = {}
    book_num = 0
    for (book_name, (book_abbrev, _)) in bible_books.items():
        book_num += 1  # "1 Thessalonians" => 52
        book_number_and_name = (
            (str(book_num)).zfill(2) + "_" + (book_name.replace(" ", "-").casefold())
        )
        # "1 Thessalonians" => "52_1-thessalonians"
        book_numbers_and_names[book_abbrev] = book_number_and_name

    readings_for = cal_date[0:2] + cal_date[3:5] + cal_date[6:9]
    with open(readings_for + "." + m3u_ext, "w") as write_file:
        write_file.write("#EXTM3U\n")
        for full_ref in full_refs:

            pattern_book1 = r"([1-3A-Z][A-Za-z][a-z] \d{1,3})"
            # "Lev 27", "1Sa 31", etc.

            pattern_book2 = r"([1-3A-Z][A-Za-z][a-z] \d{1,3})"
            # "Num 1", , "2Sa 1", etc.

            pattern = f"{pattern_book1}(-){pattern_book2}"
            match = re.search(pattern, full_ref)
            if match:  # full_ref references 1 chapter each from 2 consecutive books:
                #    Lev 27-Num 1	Jdg 21-Rut 1	Lam 5-Ezk 1
                #    Ezk 48-Dan 1	Dan 12-Hos 1	Hos 14-Jol 1
                #    Amo 9-Oba 1	    Mic 7-Nam 1	    Hab 3-Zep 1

                # Handle 1st reference of exactly 1 chapter
                (
                    _,
                    book_number_and_name,
                    book_num,
                    chapter_verse_ref,
                ) = get_book_chapter_verse(match.group(1))

                reading = book_number_and_name + "_" + chapter_verse_ref
                write_file.write("#EXTINF:-1,unknown - " + reading + "\n")
                write_file.write(
                    mp3_path + book_number_and_name + "/" + reading + ".mp3\n"
                )

                # Handle 2nd reference of exactly 1 chapter
                (
                    _,
                    book_number_and_name,
                    book_num,
                    chapter_verse_ref,
                ) = get_book_chapter_verse(match.group(3))

                reading = book_number_and_name + "_" + chapter_verse_ref
                write_file.write("#EXTINF:-1,unknown - " + reading + "\n")
                write_file.write(
                    mp3_path + book_number_and_name + "/" + reading + ".mp3\n"
                )

            else:  # full_ref only contains references within the same book

                (
                    _,
                    book_number_and_name,
                    book_num,
                    chapter_verse_ref,
                ) = get_book_chapter_verse(full_ref)

                pattern1 = r"([1-3A-Z][A-Za-z][a-z] )(\d{1,3})(-)(\d{1,3})"  # "Psa 1-2"
                match1 = re.search(pattern1, full_ref)
                # Handle readings with multiple chapters in the same book:
                #   "Gen 1-2"     -> "01_gen_1" and "01_gen_2"
                #   "Psa 1-2"     -> "19_psalm_1" and "19_psalm_2"
                #   "Psa 52-54"   -> "19_psalm_52", 19_psalm_53", and "19_psalm_54"
                #   "Psa 123-125" -> "19_psalm_123", 19_psalm_124", and "19_psalm_125"
                #   "1Sa 12-13"   -> "09_1-samuel_012" and "09_1-samuel_013"

                pattern2 = r"([1-3A-Z][A-Za-z][a-z] )(\d{1,3})(\:\d{1,3}\-)(\d{1,3})(\:)(\d{1,3})"
                match2 = re.search(pattern2, full_ref)

                if match1 or match2:
                    start_chapter = int(match1.group(2) if match1 else match2.group(2))
                    end_chapter = int(match1.group(4) if match1 else match2.group(4))
                    for chapter in range(start_chapter, end_chapter + 1):
                        chapter_ref = (str(chapter)).zfill(3 if book_num <= "39" else 2)
                        reading = book_number_and_name + "_" + chapter_ref
                        write_file.write("#EXTINF:-1,unknown - " + reading + "\n")
                        write_file.write(
                            mp3_path + book_number_and_name + "/" + reading + ".mp3\n"
                        )
                else:
                    pattern = r"(\d{1,3})(:\d{1,3}-\d{1,3})"
                    match = re.search(pattern, chapter_verse_ref)
                    if match:
                        # Handle partial chapters: Psa 78:1-37, Psa 119:1-24,
                        #   Pro 8:1-18, Mat 26:1-35, Luk 1:39-80, etc.
                        # by omitting verse references (Psa 119:1-24 -> 19_psalms_119)
                        chapter_ref = (match.group(1)).zfill(
                            3 if book_num <= "39" else 2
                        )
                        reading = book_number_and_name + "_" + chapter_ref
                    else:
                        # Handle readings of 1 full chapter:
                        #   "Psa 1" -> "19_psalm_1"
                        #   "Mat 1" -> "40_matthew_1"
                        reading = book_number_and_name + "_" + chapter_verse_ref

                        # TODO: Still need to properly handle readings w. mixed references:
                        #   Psa 105:38-45;106:1-13, Psa 117;118:1-14, Psa 133;134;135:1-12, etc.
                        # Currently, for all 3 of those references, only Psalms 105, 118,
                        # and 135 are included.
                        # HowTo: Split each full_ref at the ";",
                        #   then handle each piece of the reference separately
                        #   (Use functions to to handle the different types of references.)

                    write_file.write("#EXTINF:-1,unknown - " + reading + "\n")
                    write_file.write(
                        mp3_path + book_number_and_name + "/" + reading + ".mp3\n"
                    )

        write_file.write("#EXTINF:244,<unknown")


# Example of a similar MP3 playlist taken from my Nexus 6P:
comment = """
#EXTM3U
#EXTINF:-1,unknown - 19_psalms_002
/storage/emulated/0/Music/Bible-Audio/19_psalms/19_psalms_002.mp3
#EXTINF:-1,unknown - 40_Matthew_03
/storage/emulated/0/Music/Bible-Audio/40_matthew/40_Matthew_03.mp3
#EXTINF:237,<unknown> - 01_genesis_005
/storage/emulated/0/Music/Bible-Audio/01_genesis/01_genesis_005.mp3
#EXTINF:244,<unknown
"""
