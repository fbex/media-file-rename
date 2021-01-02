import sys

import renamedia.main as testee


def test_main_parses_args_and_calls_core_method(mocker):
    mocker.patch.object(sys, 'argv', ['renamedia.py', '-d' 'some/dir', '-v'])
    mock_find_and_rename_media_files = mocker.patch(
        'renamedia.main.core.find_and_rename_media_files'
    )
    mock_set_verbose_enabled = mocker.patch(
        'renamedia.main.settings.set_verbose_enabled'
    )

    assert testee.main() == 0
    mock_find_and_rename_media_files.assert_called_once_with('some/dir')
    mock_set_verbose_enabled.assert_called_once_with(True)


def test_parse_args_no_arguments_defaults():
    args = testee._parse_args([])
    assert args.directory == '.'
    assert args.verbose is False


def test_parse_args_directory_short():
    args = testee._parse_args(['-d', 'some/dir'])
    assert args.directory == 'some/dir'


def test_parse_args_directory_long():
    args = testee._parse_args(['--directory', 'some/other/dir'])
    assert args.directory == 'some/other/dir'


def test_parse_args_verbose_short():
    args = testee._parse_args(['-v'])
    assert args.verbose is True


def test_parse_args_verbose_long():
    args = testee._parse_args(['--verbose'])
    assert args.verbose is True


def test_parse_args_all_arguments():
    args = testee._parse_args(['-d', 'some/dir', '-v'])
    assert args.directory == 'some/dir'
    assert args.verbose is True
