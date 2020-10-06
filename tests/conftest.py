from typing import List

import pytest

from common.model import MediaType, TvMediaItem
from tmdb.model import TmdbItem, TvEpisode


@pytest.fixture
def tv_media_items() -> List[TvMediaItem]:
    return [
        TvMediaItem(
            name='Title',
            season_number='01',
            episode_number='01',
            file_extension='mkv',
            original_filename='Title.S01E01.mkv',
            episode_name='Episode 1'
        ),
        TvMediaItem(
            name='Title',
            season_number='01',
            episode_number='02',
            file_extension='mkv',
            original_filename='Title.S01E02.mkv',
            episode_name='Episode 2'
        ),
        TvMediaItem(
            name='Title',
            season_number='01',
            episode_number='03',
            file_extension='mkv',
            original_filename='Title.S01E03.mkv',
            episode_name='Episode 3'
        )
    ]


@pytest.fixture
def tmdb_item():
    return TmdbItem(
        id=4546,
        name='Title',
        type=MediaType.tv
    )


@pytest.fixture
def tv_episodes():
    return [
        TvEpisode(number=1, name='Episode 1'),
        TvEpisode(number=2, name='Episode 2'),
        TvEpisode(number=3, name='Episode 3')
    ]
