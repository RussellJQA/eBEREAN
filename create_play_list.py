# with open("Playlist.m3u8", "w") as write_file:
#     write_file.write("#EXTM3U\n")
#     write_file.write("#EXTINF:-1,unknown - 19_psalms_002\n")
#     write_file.write("/storage/emulated/0/Music/Bible-Audio/19_psalms/19_psalms_002.mp3\n")
#     write_file.write("#EXTINF:-1,unknown - 40_Matthew_03\n")
#     write_file.write("/storage/emulated/0/Music/Bible-Audio/40_matthew/40_Matthew_03.mp3\n")
#     write_file.write("#EXTINF:237,<unknown> - 01_genesis_005\n")
#     write_file.write("/storage/emulated/0/Music/Bible-Audio/01_genesis/01_genesis_005.mp3\n")
#     write_file.write("#EXTINF:244,<unknown")

from bible_books import bible_books

def create_play_list(cal_date, full_refs):

    path = "/storage/emulated/0/Music/Bible-Audio/"
    folder_names_from_abbrevs = {}
    book_num = 0
    for (book_name, (book_abbrev, chapters)) in bible_books.items():
        book_num += 1
        folder_name = book_name.lower()
        folder_name.replace(" ", "")
        folder_names_from_abbrevs[book_abbrev] = str(book_num) + "_" + folder_name

    readings_for = cal_date[0:2] + cal_date[3:5] + cal_date[6:9]
    with open("playlists/" + readings_for + ".m3u8", "w") as write_file:
        write_file.write("#EXTM3U\n")
        for full_ref in full_refs:
            book_abbr = full_ref[0:3]
            folder_name = folder_names_from_abbrevs[book_abbr]
            reading = full_ref.replace(" ", "")
                # "Psa 1" -> "Psa1"
                # "Gen 1-2" -> "Gen1-2"
            reading = reading.lower()
            write_file.write("#EXTINF:-1,unknown - " + reading + "\n")
            write_file.write(path + folder_name + "/" + reading + ".mp3\n")
        write_file.write("#EXTINF:244,<unknown")




