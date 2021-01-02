import renamedia.common.settings as testee


def test_verbose_enabled_defaults_to_false():
    assert testee.VERBOSE_ENABLED is False


def test_set_verbose_enabled():
    assert testee.VERBOSE_ENABLED is False
    testee.set_verbose_enabled(True)
    assert testee.VERBOSE_ENABLED is True
    testee.set_verbose_enabled(False)
    assert testee.VERBOSE_ENABLED is False


def test_is_verbose_enabled():
    testee.VERBOSE_ENABLED = False
    assert testee.is_verbose_enabled() is False


def test_is_verbose_disabled():
    testee.VERBOSE_ENABLED = True
    assert testee.is_verbose_enabled() is True
