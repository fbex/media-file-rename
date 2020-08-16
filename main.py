import os
import re
import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import requests
from requests import Response

media_detection_regex = '.+?(?=[sS]([0-9]{2})[eE]([0-9]{2}))'
file_output_pattern = '{name} - s{season}e{episode} - {episode_name}.{extension}'

tmdb_url = 'https://api.themoviedb.org/3'
tmdb_api_key = os.environ['TMDB_API_KEY']

parser = ArgumentParser(description='Gather release information for a given week.')
parser.add_argument('-d', '--directory',
                    metavar='<directory>',
                    type=str,
                    default='',
                    help='The working directory to use')
parser.add_argument('-v', '--verbose',
                    action='store_true')
args = parser.parse_args()


@dataclass
class MediaItem:
    name: str
    season: str
    episode: str
    extension: str
    original_filename: str
    episode_name: str = None

    def filename(self) -> str:
        return file_output_pattern \
            .format(name=self.name, season=self.season, episode=self.episode,
                    episode_name=self.episode_name, extension=self.extension)


class MediaType(Enum):
    tv = 'tv'
    movie = 'movie'


@dataclass
class TmdbItem:
    id: int
    name: str
    type: MediaType


@dataclass
class TvEpisode:
    number: int
    name: str


def main():
    if args.directory:
        os.chdir(args.directory)
    files = os.listdir()
    media_items = get_media_items(files)
    print("Matched {} files to {} media items:".format(len(files), len(media_items)))
    for item in media_items:
        print(item.filename())
    continue_answer = input("Do you want to rename these files? (Y/n): ").lower()
    if continue_answer != 'n':
        rename_items(media_items)
        print("Renamed {} files".format(len(media_items)))


def get_media_items(files: List[str]) -> List[MediaItem]:
    media_items = [detect_media(file) for file in files]
    media_items = filter_not_none_items(media_items)
    if len(media_items) == 0:
        print("No media items found")
        sys.exit()
    media_items.sort(key=get_episode)
    # TODO: sanity check: all items have the same name and season
    enrich_media_items(media_items)
    return media_items


def enrich_media_items(media_items: List[MediaItem]):
    tmdb_item = find_tmdb_item(media_items[0])
    if tmdb_item.type is MediaType.tv:
        episodes = get_tmdb_episodes_for_season(tmdb_item, media_items[0].season)
        for item in media_items:
            item.episode_name = find_episode_by_number(int(item.episode), episodes).name


def find_episode_by_number(number: int, tv_episode: List[TvEpisode]) -> Optional[TvEpisode]:
    for item in tv_episode:
        if item.number == number:
            return item
    return None


def find_tmdb_item(media_item: MediaItem) -> TmdbItem:
    search_url = '{url}/search/multi'.format(url=tmdb_url)
    params = {
        "api_key": tmdb_api_key,
        "language": "en-US",
        "page": 1,
        "include_adult": "false",
        "query": media_item.name
    }
    r = requests.get(url=search_url, params=params)
    handle_request_error(r)
    first_result = r.json()['results'][0]
    name = first_result['name']
    media_type = first_result['media_type']
    tmdb_id = first_result['id']
    verbose_print("Found tmdb item: {}, {}, {}".format(name, media_type, tmdb_id))
    if name != media_item.name:
        print("No media information found for title [{}]".format(media_item.name))
        sys.exit()  # TODO: Provide custom input for search query...
    return TmdbItem(id=tmdb_id, name=name, type=MediaType[media_type])


def get_tmdb_episodes_for_season(tmdb_item: TmdbItem, season_number: str) -> List[TvEpisode]:
    tv_url = '{url}/tv/{tv_id}/season/{season_number}'.format(url=tmdb_url, tv_id=tmdb_item.id,
                                                              season_number=season_number)
    params = {
        "api_key": tmdb_api_key,
        "language": "en-US"
    }
    r = requests.get(url=tv_url, params=params)
    handle_request_error(r)
    episodes = r.json()['episodes']
    return [TvEpisode(number=episode['episode_number'], name=episode['name']) for episode in episodes]


def handle_request_error(r: Response):
    if r.status_code != 200:
        verbose_print("Error obtaining media information, because: {}".format(r.reason))
        verbose_print("Response was [{}] with content: [{}]".format(r.status_code, r.json()))


def filter_not_none_items(items: List[MediaItem]) -> List[MediaItem]:
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


def verbose_print(text: str):
    if args.verbose:
        print(text)


if __name__ == '__main__':
    main()
