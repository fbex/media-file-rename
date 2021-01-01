from typing import List

from renamedia.common.model import TvMediaItem
from renamedia.rename import io, media


def find_and_rename_media_files(directory: str):
    io.chdir(directory)
    files = io.listdir()
    media_items = media.detect_media_items(files)
    _print_found_items(files, media_items)
    if _should_continue():
        _rename_items(media_items)
        print("Renamed {} files".format(len(media_items)))


def _print_found_items(files: List[str], media_items: List[TvMediaItem]):
    print(
        ("Matched {} files to {} media items:"
         .format(len(files), len(media_items)))
    )
    for item in media_items:
        print(item.filename())


def _should_continue() -> bool:
    answer = input("Do you want to rename these files? (Y/n): ").lower()
    if answer == 'n':
        return False
    else:
        return True


def _rename_items(media_items: List[TvMediaItem]):
    for item in media_items:
        io.rename(item.original_filename, item.filename())
