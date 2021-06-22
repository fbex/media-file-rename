from typing import List

import pytest

import renamedia.rename.media as testee
from renamedia.common.model import MediaType, TvMediaItem
from renamedia.tmdb.model import TmdbItem, TvEpisode


def test_detect_media_items_empty_filenames():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        testee.detect_media_items([])
    assert pytest_wrapped_e.type == SystemExit


def test_detect_media_items_wrong_filenames():
    filenames = ['wrong.filename', '']
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        testee.detect_media_items(filenames)
    assert pytest_wrapped_e.type == SystemExit


def test_detect_media_items_enrich_and_sort(
        mock_tmdb_item, mock_tv_episodes, tv_media_items
):
    filenames = ['Title.S01E02.mkv', 'Title.S01E03.mkv', 'Title.S01E01.mkv']
    assert testee.detect_media_items(filenames) == tv_media_items


@pytest.mark.parametrize('filename, title, season, episode, extension', [
    ('A.S01E01.mkv', 'A', '01', '01', 'mkv'),
    ('1.S01E01.mkv', '1', '01', '01', 'mkv'),
    ('Title.S01E01.mkv', 'Title', '01', '01', 'mkv'),
    ('Title.So.And.So.S01E01.mkv', 'Title So And So', '01', '01', 'mkv'),
    ('Title.S10E01.mp4', 'Title', '10', '01', 'mp4'),
    ('Title..s01e01.mkv', 'Title', '01', '01', 'mkv'),
    ('Title.S01E10.mkv', 'Title', '01', '10', 'mkv'),
    ('Title.S10E10.mkv', 'Title', '10', '10', 'mkv'),
    ('A.S01E01.avi', 'A', '01', '01', 'avi')
])
def test_extract_media_item_from_filename(
        filename, title, season, episode, extension
):
    expected = TvMediaItem(
        name=title,
        season_number=season,
        episode_number=episode,
        file_extension=extension,
        original_filename=filename
    )

    result = testee._extract_media_item_from_filename(filename)

    assert result == expected


@pytest.mark.parametrize('filename', [
    'Title.S01.mkv',
    'Title.E01.mkv',
    'S01E01',
    'S01E01.mkv',
    'aS01E01.mkv',
    '1S01E01.mkv',
    '.S01E01.mkv',
])
def test_extract_media_item_from_filename_no_match(filename):
    result = testee._extract_media_item_from_filename(filename)

    assert result is None


def test_enrich_media_items_episode_name_none_for_movie(
        mock_tmdb_item, tv_media_items
):
    mock_tmdb_item.type = MediaType.movie
    tv_media_items[0].episode_name = None

    testee._enrich_media_items(tv_media_items)

    assert tv_media_items[0].episode_name is None


def test_enrich_media_items_episode_name_for_tv_show(
        mock_tmdb_item, mock_tv_episodes, tv_media_items
):
    for item in tv_media_items:
        item.episode_name = None

    testee._enrich_media_items(tv_media_items)

    assert tv_media_items[0].episode_name == 'Episode 1'
    assert tv_media_items[1].episode_name == 'Episode 2'
    assert tv_media_items[2].episode_name == 'Episode 3'


def test_enrich_media_items_episode_not_found(
        mock_tmdb_item, mock_tv_episodes, tv_media_items
):
    for item in tv_media_items:
        item.episode_name = None
        item.episode_number = 99

    testee._enrich_media_items(tv_media_items)

    assert tv_media_items[0].episode_name is None


def test_enrich_media_items_episode_name_for_empty_input():
    # assert no error with empty list
    testee._enrich_media_items([])


@pytest.fixture
def mock_tmdb_item(mocker, tmdb_item) -> TmdbItem:
    mocker.patch('renamedia.tmdb.client.find', return_value=tmdb_item)
    return tmdb_item


@pytest.fixture
def mock_tv_episodes(mocker, tv_episodes) -> List[TvEpisode]:
    mocker.patch(
        'renamedia.tmdb.client.get_episodes_for_season',
        return_value=tv_episodes
    )
    return tv_episodes
