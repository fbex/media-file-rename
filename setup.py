import codecs
import os
import pathlib
import re

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

install_requires = ['requests']
tests_require = ['pytest', 'pytest-mock', 'responses']


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


NAME = "renamedia"

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    META_PATH
except NameError:
    META_PATH = os.path.join(HERE, "src/rename", "__init__.py")
finally:
    META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


setup(
    name="renamedia",
    version=find_meta("version"),
    description='Rename media files inside a given directory',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fbex/media-file-rename',
    author='fbex',
    author_email='fbex@github.com',
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='media, file, rename, tmdb, movie, tv, show',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.7, <4',
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points={
        "console_scripts": [
            "renamedia = rename.__main__:main"
        ]
    },
)
