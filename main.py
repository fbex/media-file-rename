import os
import re
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import List

media_detection_regex = '.+?(?=[sS]([0-9]{2})[eE]([0-9]{2}))'
file_output_pattern = '{name} - s{season}e{episode}.{extension}'

parser = ArgumentParser(description='Gather release information for a given week.')
parser.add_argument('-d', '--directory',
                    metavar='<directory>',
                    type=str,
                    default='',
                    help='The working directory to use')
args = parser.parse_args()


@dataclass
class MediaItem:
    name: str
    season: str
    episode: str
    extension: str
    original_filename: str

    def filename(self) -> str:
        return file_output_pattern \
            .format(name=self.name, season=self.season, episode=self.episode, extension=self.extension)


def main():
    if args.directory:
        os.chdir(args.directory)
    files = os.listdir()
    media_items = get_media_items(files)
    if len(media_items) == 0:
        print("No media items found")
        return
    print("Matched {} files to {} media items:".format(len(files), len(media_items)))
    for item in media_items:
        print(item.filename())
    continue_answer = input("Do you want to rename these files? (Y/n): ").lower()
    if continue_answer != 'n':
        rename_items(media_items)
        print("Renamed {} files".format(len(media_items)))


def get_media_items(files: List[str]) -> List[MediaItem]:
    media_items = [detect_media(file) for file in files]
    media_items = filter_items(media_items)
    media_items.sort(key=get_episode)
    return media_items


def filter_items(items: List[MediaItem]) -> List[MediaItem]:
    return [item for item in items if item is not None]


def get_episode(item: MediaItem) -> str:
    return item.episode


def detect_media(filename: str) -> MediaItem:
    media_set = re.search(media_detection_regex, filename)
    if media_set is not None and len(media_set.groups()) == 2:
        name = media_set.group(0).replace('.', ' ').strip()
        season = media_set.group(1)
        episode = media_set.group(2)
        return MediaItem(name, season, episode, 'mkv', filename)


def rename_items(media_items: List[MediaItem]):
    for item in media_items:
        os.rename(item.original_filename, item.filename())


if __name__ == '__main__':
    main()
