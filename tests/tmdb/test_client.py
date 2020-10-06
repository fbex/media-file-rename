import pytest
import responses

import tmdb.client as testee

_FIND_URL = ('https://api.themoviedb.org/3/search/multi?api_key=12345'
             '&language=en-US&page=1&include_adult=false&query=Title')
_GET_URL = ('https://api.themoviedb.org/3/tv/4546/season/01'
            '?api_key=12345&language=en-US')


@pytest.fixture
def mock_env(mocker):
    mocker.patch.dict('os.environ', {"TMDB_API_KEY": "12345"})


@responses.activate
def test_find_single_result(mock_env, tv_media_items, tmdb_item):
    responses.add(
        responses.GET,
        _FIND_URL,
        json={
            "page": 1,
            "total_results": 0,
            "total_pages": 0,
            "results": [
                {
                    "original_name": "Title",
                    "genre_ids": [
                        35
                    ],
                    "media_type": "tv",
                    "name": "Title",
                    "popularity": 36.208,
                    "origin_country": [
                        "US"
                    ],
                    "vote_count": 368,
                    "first_air_date": "2000-10-15",
                    "backdrop_path": "/eNSIkGIYqXVFNmT85P4X7BsXkYI.jpg",
                    "original_language": "en",
                    "id": 4546,
                    "vote_average": 8.1,
                    "overview": "The off-kilter, unscripted comic ...",
                    "poster_path": "/kWQDOnLs5DK0ta8xQZLsaienIHp.jpg"
                }
            ]
        },
        status=200,
        match_querystring=True
    )

    actual = testee.find(tv_media_items[0])

    assert actual == tmdb_item


@responses.activate
def test_find_multiple_results(mock_env, tv_media_items, tmdb_item):
    responses.add(
        responses.GET,
        _FIND_URL,
        json={
            "page": 1,
            "total_results": 0,
            "total_pages": 0,
            "results": [
                {
                    "original_name": "Title",
                    "genre_ids": [
                        35
                    ],
                    "media_type": "tv",
                    "name": "Title",
                    "popularity": 36.208,
                    "origin_country": [
                        "US"
                    ],
                    "vote_count": 368,
                    "first_air_date": "2000-10-15",
                    "backdrop_path": "/eNSIkGIYqXVFNmT85P4X7BsXkYI.jpg",
                    "original_language": "en",
                    "id": 4546,
                    "vote_average": 8.1,
                    "overview": "The off-kilter, unscripted comic ...",
                    "poster_path": "/kWQDOnLs5DK0ta8xQZLsaienIHp.jpg"
                },
                {
                    "original_name": "The Sopranos",
                    "genre_ids": [
                        18
                    ],
                    "media_type": "tv",
                    "name": "The Sopranos",
                    "popularity": 51.79,
                    "origin_country": [
                        "US"
                    ],
                    "vote_count": 1162,
                    "first_air_date": "1999-01-10",
                    "backdrop_path": "/3ltpFyIfAtGjRMRJdECFoQQCfzx.jpg",
                    "original_language": "en",
                    "id": 1398,
                    "vote_average": 8.4,
                    "overview": "The story of New Jersey-based ...",
                    "poster_path": "/6nNZnnUkXcI3DvdrkclulanYXzg.jpg"
                }
            ]
        },
        status=200,
        match_querystring=True
    )

    actual = testee.find(tv_media_items[0])

    assert actual == tmdb_item


@responses.activate
def test_find_no_results(mock_env, tv_media_items):
    responses.add(
        responses.GET,
        _FIND_URL,
        json={
            "page": 1,
            "total_results": 0,
            "total_pages": 0,
            "results": []
        },
        status=200,
        match_querystring=True
    )

    with pytest.raises(ValueError) as error:
        testee.find(tv_media_items[0])

    assert (error.value.args[0] ==
            'No media information found for title [Title]')


@responses.activate
def test_find_not_found(mock_env, tv_media_items):
    responses.add(
        responses.GET,
        _FIND_URL,
        json={
            "success": False,
            "status_code": 34,
            "status_message": "The resource you requested could not be found."
        },
        status=404,
        match_querystring=True
    )

    with pytest.raises(ValueError) as error:
        testee.find(tv_media_items[0])

    assert (error.value.args[0] ==
            'Error obtaining media information. '
            'Status: [404], reason: [Not Found]')


@responses.activate
def test_get_episodes_for_season(mock_env, tmdb_item, tv_episodes):
    responses.add(
        responses.GET,
        _GET_URL,
        json={
            "_id": "52576f03760ee36aaa44ffcf",
            "air_date": "2000-10-15",
            "episodes": [
                {
                    "air_date": "2000-10-15",
                    "episode_number": 1,
                    "id": 324160,
                    "name": "Episode 1",
                    "overview": "An innocent bunch-up in Larry's ...",
                    "production_code": "",
                    "season_number": 1,
                    "show_id": 4546,
                    "still_path": "/1bFepeqNpx940YCTh0mI2tHgZCa.jpg",
                    "vote_average": 7.167,
                    "vote_count": 12,
                },
                {
                    "air_date": "2000-10-22",
                    "episode_number": 2,
                    "id": 324162,
                    "name": "Episode 2",
                    "overview": "Larry and Cheryl's fun-filled bowling ...",
                    "production_code": "",
                    "season_number": 1,
                    "show_id": 4546,
                    "still_path": "/714jnxgQqyowldnKMmNEomzeE3j.jpg",
                    "vote_average": 7.667,
                    "vote_count": 9
                },
                {
                    "air_date": "2000-10-29",
                    "episode_number": 3,
                    "id": 324169,
                    "name": "Episode 3",
                    "overview": "Larry sets off a bizarre chain of ...",
                    "production_code": "",
                    "season_number": 1,
                    "show_id": 4546,
                    "still_path": "/3rrhO0WLNiBceTtIaVzneYbfxu0.jpg",
                    "vote_average": 8.0,
                    "vote_count": 9
                }
            ]
        },
        status=200,
        match_querystring=True
    )

    actual = testee.get_episodes_for_season(tmdb_item, '01')

    assert actual == tv_episodes


@responses.activate
def test_get_episodes_for_season_not_found(mock_env, tmdb_item, tv_episodes):
    responses.add(
        responses.GET,
        _GET_URL,
        json={
            "success": False,
            "status_code": 34,
            "status_message": "The resource you requested could not be found."
        },
        status=404,
        match_querystring=True
    )

    with pytest.raises(ValueError) as error:
        testee.get_episodes_for_season(tmdb_item, '01')

    assert (error.value.args[0] ==
            'Error obtaining media information. '
            'Status: [404], reason: [Not Found]')
