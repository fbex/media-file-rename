_VERBOSE_ENABLED = False


def set_verbose_enabled(verbose_enabled: bool):
    global _VERBOSE_ENABLED
    _VERBOSE_ENABLED = verbose_enabled


def is_verbose_enabled() -> bool:
    return _VERBOSE_ENABLED
