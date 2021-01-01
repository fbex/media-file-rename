from renamedia.common.settings import is_verbose_enabled


def verbose_print(text: str):
    if is_verbose_enabled():
        print(text)
