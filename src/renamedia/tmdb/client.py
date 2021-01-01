import os
import sys
from typing import Dict, List

import requests
from requests import Response

from renamedia.common.helpers import verbose_print
from renamedia.common.model import TvMediaItem
from renamedia.tmdb.model import MediaType, TmdbItem, TvEpisode

_TMDB_URL = 'https://api.themoviedb.org/3'


def find(media_item: TvMediaItem) -> TmdbItem:
    search_url = '{url}/search/multi'.format(url=_TMDB_URL)
    params = {
        "api_key": _get_api_key(),
        "language": "en-US",
        "page": 1,
        "include_adult": "false",
        "query": media_item.name
    }
    response = requests.get(url=search_url, params=params)
    _handle_error(response)
    results = response.json()['results']
    tmdb_item = _extract_tmdb_item(media_item, results)
    if tmdb_item.name != media_item.name:
        print(
            "No media information found for title [{}]".format(media_item.name)
        )
        sys.exit()  # TODO: Provide custom input for search query...
    return tmdb_item


def _extract_tmdb_item(media_item: TvMediaItem, results: Dict):
    if len(results) == 0:
        # TODO: Provide custom input for search query...
        raise ValueError(
            "No media information found for title [{}]".format(media_item.name)
        )
    tmdb_item = TmdbItem(
        id=results[0]['id'],
        name=results[0]['name'],
        type=MediaType[results[0]['media_type']]
    )
    verbose_print(
        "Found tmdb item: {}, {}, {}".format(
            tmdb_item.name, tmdb_item.type, tmdb_item.id
        )
    )
    return tmdb_item


def get_episodes_for_season(
        tmdb_item: TmdbItem,
        season_number: str
) -> List[TvEpisode]:
    tv_url = '{url}/tv/{tv_id}/season/{season_number}'.format(
        url=_TMDB_URL,
        tv_id=tmdb_item.id,
        season_number=season_number
    )
    params = {
        "api_key": _get_api_key(),
        "language": "en-US"
    }
    response = requests.get(url=tv_url, params=params)
    _handle_error(response)
    episodes = response.json()['episodes']
    return [
        TvEpisode(number=episode['episode_number'], name=episode['name'])
        for episode in episodes
    ]


def _handle_error(r: Response):
    if r.status_code != 200:
        verbose_print(
            "Response was [{}] with content: [{}]".format(
                r.status_code, r.json()
            )
        )
        raise ValueError(
            ("Error obtaining media information. Status: [{}], reason: [{}]"
             .format(r.status_code, r.reason, ))
        )


def _get_api_key() -> str:
    return os.environ['TMDB_API_KEY']
