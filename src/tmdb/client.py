import os
import sys
from typing import List, Optional

import requests
from requests import Response

from common.helpers import verbose_print
from common.model import TvMediaItem
from tmdb.model import MediaType, TmdbItem, TvEpisode

_tmdb_url = 'https://api.themoviedb.org/3'
_tmdb_api_key = os.environ['TMDB_API_KEY']


def find(media_item: TvMediaItem) -> TmdbItem:
    search_url = '{url}/search/multi'.format(url=_tmdb_url)
    params = {
        "api_key": _tmdb_api_key,
        "language": "en-US",
        "page": 1,
        "include_adult": "false",
        "query": media_item.name
    }
    r = requests.get(url=search_url, params=params)
    _handle_request_error(r)
    first_result = r.json()['results'][0]
    name = first_result['name']
    media_type = first_result['media_type']
    tmdb_id = first_result['id']
    verbose_print("Found tmdb item: {}, {}, {}".format(name, media_type, tmdb_id))
    if name != media_item.name:
        print("No media information found for title [{}]".format(media_item.name))
        sys.exit()  # TODO: Provide custom input for search query...
    return TmdbItem(id=tmdb_id, name=name, type=MediaType[media_type])


def get_episodes_for_season(tmdb_item: TmdbItem, season_number: str) -> List[TvEpisode]:
    tv_url = '{url}/tv/{tv_id}/season/{season_number}'.format(url=_tmdb_url, tv_id=tmdb_item.id,
                                                              season_number=season_number)
    params = {
        "api_key": _tmdb_api_key,
        "language": "en-US"
    }
    r = requests.get(url=tv_url, params=params)
    _handle_request_error(r)
    episodes = r.json()['episodes']
    return [TvEpisode(number=episode['episode_number'], name=episode['name']) for episode in episodes]


def find_episode_by_number(number: int, tv_episode: List[TvEpisode]) -> Optional[TvEpisode]:
    for item in tv_episode:
        if item.number == number:
            return item
    return None


def _handle_request_error(r: Response):
    if r.status_code != 200:
        verbose_print("Error obtaining media information, because: {}".format(r.reason))
        verbose_print("Response was [{}] with content: [{}]".format(r.status_code, r.json()))
