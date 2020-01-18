"""
Create an MP3 playlist for each day in the specified Bible reading plan.
"""

import os
import re

from lib.bible_books import bible_books


def create_bible_plan_playlists(plan, cal_date, full_refs, m3u_ext="m3u"):
    """
    An .m3u8 file is essentially the same as an .m3u file, but it's UTF-8 encoded.
    .m3u was chosen as the default extension since some platforms don't support .m3u8.
    """

    mp3_path = "/storage/emulated/0/Music/Bible-Audio/"
    book_numbers_and_names = {}
    book_num = 0
    for (book_name, (book_abbrev, chapters)) in bible_books.items():
        book_num += 1  # "1 Thessalonians" => 52
        book_number_and_name = (
            (str(book_num)).zfill(2) + "_" + (book_name.replace(" ", "-").lower())
        )
        # "1 Thessalonians" => "52_1-thessalonians"
        book_numbers_and_names[book_abbrev] = book_number_and_name

    readings_for = cal_date[0:2] + cal_date[3:5] + cal_date[6:9]
    with open(readings_for + "." + m3u_ext, "w") as write_file:
        write_file.write("#EXTM3U\n")
        for full_ref in full_refs:
            book_abbr = full_ref[0:3]
            book_number_and_name = book_numbers_and_names[book_abbr]
            book_num = book_number_and_name[0:2]
            chapter_verse_ref = full_ref[4:].zfill(3 if book_num <= "39" else 2)

            pattern = r"([1-3A-Z][a-z][a-z] )(\d{1,3})(-)(\d{1,3})"  # "Psa 1-2"
            match = re.search(pattern, full_ref)
            if match:
                # Thist section properly handles readings with multiple chapters,
                #   "Gen 1-2"     -> "01_gen_1" and "01_gen_2"
                #   "Psa 1-2"     -> "19_psalm_1" and "19_psalm_2"
                #   "Psa 52-54"   -> "19_psalm_52", 19_psalm_53", and "19_psalm_54"
                #   "Psa 123-125" -> "19_psalm_123", 19_psalm_124", and "19_psalm_125"
                initial_chapter = int(match.group(2))
                final_chapter = int(match.group(4))
                for chapter in range(initial_chapter, final_chapter + 1):
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
                    # This handles partial chapters: Psa 78:1-37, Psa 119:1-24,
                    #   Pro 8:1-18, Mat 26:1-35, Luk 1:39-80, etc.
                    # by omitting verse references (Psa 119:1-24 -> 19_psalms_119)
                    chapter_ref = (match.group(1)).zfill(3 if book_num <= "39" else 2)
                    reading = book_number_and_name + "_" + chapter_ref
                else:
                    # This properly handles readings of 1 full chapter:
                    #   "Psa 1" -> "19_psalm_1"
                    #   "Mat 1" -> "40_matthew_1"
                    reading = book_number_and_name + "_" + chapter_verse_ref

                    # TODO: Still need to properly handle readings w. mixed references:
                    #   Psa 105:38-45;106:1-13, Psa 117;118:1-14, Psa 133;134;135:1-12, etc.
                    # Currently, for all 3 of those references, only Psalms 105, 118,
                    # and 135 are included.
                    # HowTo: Split each full_ref at the ";",
                    #   then handle each piced of the reference separately
                    #   (Use functions to to handle the different types of references.)

                write_file.write("#EXTINF:-1,unknown - " + reading + "\n")
                write_file.write(
                    mp3_path + book_number_and_name + "/" + reading + ".mp3\n"
                )

        write_file.write("#EXTINF:244,<unknown")


# Example of a similar MP3 playlist taken from my Nexus 6P:
"""
#EXTM3U
#EXTINF:-1,unknown - 19_psalms_002
/storage/emulated/0/Music/Bible-Audio/19_psalms/19_psalms_002.mp3
#EXTINF:-1,unknown - 40_Matthew_03
/storage/emulated/0/Music/Bible-Audio/40_matthew/40_Matthew_03.mp3
#EXTINF:237,<unknown> - 01_genesis_005
/storage/emulated/0/Music/Bible-Audio/01_genesis/01_genesis_005.mp3
#EXTINF:244,<unknown
"""
