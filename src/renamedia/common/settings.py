VERBOSE_ENABLED = False


def set_verbose_enabled(verbose_enabled: bool):
    global VERBOSE_ENABLED
    VERBOSE_ENABLED = verbose_enabled


def is_verbose_enabled() -> bool:
    return VERBOSE_ENABLED
