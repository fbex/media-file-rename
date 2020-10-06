from unittest import mock

import rename.io as testee


def test_listdir(mocker):
    expected = ['foo', 'bar']
    mocker.patch('os.listdir', return_value=expected)

    assert testee.listdir() == expected


@mock.patch('os.chdir')
def test_chdir(os_chdir):
    testee.chdir('foo')
    os_chdir.assert_called_once_with('foo')


@mock.patch('os.rename')
def test_rename(os_rename):
    testee.rename('orig', 'new')
    os_rename.assert_called_once_with('orig', 'new')
