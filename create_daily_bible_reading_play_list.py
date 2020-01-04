"""
Create a daily MP3 playlist for each day in a Bible reading plan.
"""

from bible_books import bible_books

def create_daily_bible_reading_play_list(cal_date, full_refs):

    path = "/storage/emulated/0/Music/Bible-Audio/"
    book_numbers_and_names = {}
    book_num = 0
    for (book_name, (book_abbrev, chapters)) in bible_books.items():
        book_num += 1  # "1 Thessalonians" => 52
        book_number_and_name = str(book_num) + "_" + book_name.replace(" ", "-").lower()
        # "1 Thessalonians" => "52_1-thessalonians"
        book_numbers_and_names[book_abbrev] = book_number_and_name

    readings_for = cal_date[0:2] + cal_date[3:5] + cal_date[6:9]
    with open("playlists/" + readings_for + ".m3u8", "w") as write_file:
        write_file.write("#EXTM3U\n")
        for full_ref in full_refs:
            book_abbr = full_ref[0:3]
            book_number_and_name = book_numbers_and_names[book_abbr]
            book_num = book_number_and_name[0:2]
            chapter_verse_ref = full_ref[4:].zfill(3 if book_num <= "39" else 2)
            reading = book_number_and_name + '_' + chapter_verse_ref
                # "Gen 1-2" -> "01_gen_1-2"
                # "Psa 1" -> "19_psalm_1"
                # "Mat 1" -> "40_matthew_1"
            write_file.write("#EXTINF:-1,unknown - " + reading + "\n")
            write_file.write(path + book_number_and_name + "/" + reading + ".mp3\n")
        write_file.write("#EXTINF:244,<unknown")

# with open("Playlist.m3u8", "w") as write_file:
#     write_file.write("#EXTM3U\n")
#     write_file.write("#EXTINF:-1,unknown - 19_psalms_002\n")
#     write_file.write("/storage/emulated/0/Music/Bible-Audio/19_psalms/19_psalms_002.mp3\n")
#     write_file.write("#EXTINF:-1,unknown - 40_Matthew_03\n")
#     write_file.write("/storage/emulated/0/Music/Bible-Audio/40_matthew/40_Matthew_03.mp3\n")
#     write_file.write("#EXTINF:237,<unknown> - 01_genesis_005\n")
#     write_file.write("/storage/emulated/0/Music/Bible-Audio/01_genesis/01_genesis_005.mp3\n")
#     write_file.write("#EXTINF:244,<unknown")
