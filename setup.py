import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="media_file_rename",
    version="0.0.1",
    description='Rename media files inside a directory',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fbex/media-file-rename',
    author='fbex',
    author_email='fbex@github.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='media, file, rename, tmdb, movie, tv, show',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    install_requires=['requests'],
    entry_points={
        "console_scripts": [
            "media-rename = rename.__main__:main"
        ]
    },
)
