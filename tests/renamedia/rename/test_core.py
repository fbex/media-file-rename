from unittest.mock import call

import pytest

import renamedia.rename.core as testee


def test_find_and_rename_media_files(mocker, capsys, tv_media_items):
    files = ['Title.S01E01.mkv', 'Title.S01E02.mkv', 'Title.S01E03.mkv']
    mocker.patch('renamedia.rename.io.listdir', return_value=files)
    mocker.patch('renamedia.rename.core._should_continue', return_value=True)
    mocker.patch(
        'renamedia.rename.media.detect_media_items',
        return_value=tv_media_items
    )
    io_chdir = mocker.patch('renamedia.rename.io.chdir')
    io_rename = mocker.patch('renamedia.rename.io.rename')

    testee.find_and_rename_media_files('.')

    captured = capsys.readouterr()
    assert captured.out == (
        'Matched 3 files to 3 media items:\n'
        'Title - s01e01 - Episode 1.mkv\n'
        'Title - s01e02 - Episode 2.mkv\n'
        'Title - s01e03 - Episode 3.mkv\n'
        'Renamed 3 files\n'
    )

    io_chdir.assert_called_once_with('.')
    io_rename.assert_has_calls([
        call(files[0], tv_media_items[0].filename()),
        call(files[1], tv_media_items[1].filename()),
        call(files[2], tv_media_items[2].filename())
    ])


def test_find_and_rename_media_files_dont_rename(
        mocker, capsys, tv_media_items
):
    files = ['Title.S01E01.mkv']
    mocker.patch('renamedia.rename.io.listdir', return_value=files)
    mocker.patch('renamedia.rename.core._should_continue', return_value=False)
    mocker.patch(
        'renamedia.rename.media.detect_media_items',
        return_value=[tv_media_items[0]]
    )
    io_chdir = mocker.patch('renamedia.rename.io.chdir')
    io_rename = mocker.patch('renamedia.rename.io.rename')

    testee.find_and_rename_media_files('directory')

    captured = capsys.readouterr()
    assert captured.out == (
        'Matched 1 files to 1 media items:\n'
        'Title - s01e01 - Episode 1.mkv\n'
    )

    io_chdir.assert_called_once_with('directory')
    io_rename.assert_not_called()


@pytest.mark.parametrize('input_value, expected', [
    ('Y', True),
    ('y', True),
    ('N', False),
    ('n', False),
    ('', True),
    ('x', True),
    ('xx', True),
])
def test__should_continue(mocker, input_value, expected):
    mocker.patch('builtins.input', return_value=input_value)
    assert testee._should_continue() is expected
