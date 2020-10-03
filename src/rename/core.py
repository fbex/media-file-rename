from typing import List

import rename.io as io
import rename.media as media
from common import args
from common.model import TvMediaItem


def find_and_rename_media_files():
    if args.directory:
        io.chdir(args.directory)
    files = io.listdir()
    media_items = media.detect_media_items(files)
    print("Matched {} files to {} media items:".format(len(files),
                                                       len(media_items)))
    for item in media_items:
        print(item.filename())
    continue_answer = input(
        "Do you want to rename these files? (Y/n): ").lower()
    if continue_answer != 'n':
        _rename_items(media_items)
        print("Renamed {} files".format(len(media_items)))


def _rename_items(media_items: List[TvMediaItem]):
    for item in media_items:
        io.rename(item.original_filename, item.filename())
