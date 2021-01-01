import os
from typing import List


def listdir() -> List[str]:
    return os.listdir()


def chdir(directory):
    os.chdir(directory)


def rename(filename: str, new_filename: str):
    os.rename(filename, new_filename)
