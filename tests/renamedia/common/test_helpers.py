import renamedia.common.helpers as testee


def test_verbose_print_enabled(mocker, capsys):
    mocker.patch('renamedia.common.helpers.is_verbose_enabled',
                 return_value=True)

    testee.verbose_print('verbose is enabled')

    captured = capsys.readouterr()
    assert captured.out == 'verbose is enabled\n'


def test_verbose_print_disabled(mocker, capsys):
    mocker.patch('renamedia.common.helpers.is_verbose_enabled',
                 return_value=False)

    testee.verbose_print('verbose is disabled')

    captured = capsys.readouterr()
    assert captured.out == ''
