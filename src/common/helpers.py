from common import args


def verbose_print(text: str):
    if args.verbose:
        print(text)
