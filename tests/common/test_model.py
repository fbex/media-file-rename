import pytest


def test_tv_media_item_get_episode_number(tv_media_items):
    episode_number = tv_media_items[0].get_episode_number()
    assert episode_number == tv_media_items[0].episode_number


@pytest.mark.parametrize('index, expected', [
    (0, 'Title - s01e01 - Episode 1.mkv'),
    (1, 'Title - s01e02 - Episode 2.mkv'),
    (2, 'Title - s01e03 - Episode 3.mkv')
])
def test_tv_media_item_filename(tv_media_items, index, expected):
    assert tv_media_items[index].filename() == expected
