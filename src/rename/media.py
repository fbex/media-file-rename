import re
import sys
from typing import List

import tmdb.client as tmdb_client
from common.model import MediaType, TvMediaItem

_media_detection_regex = '.+?(?=[sS]([0-9]{2})[eE]([0-9]{2}))'


def detect_media_items(filenames: List[str]) -> List[TvMediaItem]:
    media_items = [_detect_media_in_file(file) for file in filenames]
    media_items = _filter_not_none_items(media_items)
    if len(media_items) == 0:
        print("No media items found")
        sys.exit()
    media_items.sort(key=TvMediaItem.get_episode_number)
    # TODO: sanity check: all items have the same name and season
    _enrich_media_items(media_items)
    return media_items


def _detect_media_in_file(filename: str) -> TvMediaItem:
    media_set = re.search(_media_detection_regex, filename)
    if media_set is not None and len(media_set.groups()) == 2:
        name = media_set.group(0).replace('.', ' ').strip()
        season = media_set.group(1)
        episode = media_set.group(2)
        # TODO: detect fileextension instead of hardcoding it
        return TvMediaItem(name, season, episode, 'mkv', filename)


def _enrich_media_items(media_items: List[TvMediaItem]):
    tmdb_item = tmdb_client.find(media_items[0])
    if tmdb_item.type is MediaType.tv:
        episodes = tmdb_client.get_episodes_for_season(
            tmdb_item, media_items[0].season_number)
        for item in media_items:
            item.episode_name = tmdb_client.find_episode_by_number(
                int(item.episode_number), episodes).name


def _filter_not_none_items(items: List[TvMediaItem]) -> List[TvMediaItem]:
    return [item for item in items if item is not None]
