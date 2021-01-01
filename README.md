# media-file-rename

[![CI](https://github.com/fbex/media-file-rename/workflows/CI/badge.svg?branch=master)](https://github.com/fbex/media-file-rename/actions?workflow=CI)
[![codecov](https://codecov.io/gh/fbex/media-file-rename/branch/master/graph/badge.svg?token=L1ow3vRrMR)](https://codecov.io/gh/fbex/media-file-rename)

A script to detect media files inside a given directory and rename them by a certain pattern.
Media files are enriched with information from TMDB.

Note that the script currently only supports TV shows and no movies.

## How to run

Requires a TMDB api key in an environment variable: `export TMDB_API_KEY=<api-key>`.
To get an API key, simply register an account at https://www.themoviedb.org.

Set up a venv (e.g. with pyenv-virtualenv) and install this package: `pip install .`

Run the module with `python -m renamedia` or the console script with `renamedia` from within the venv.

## How to develop

Install and setup pyenv with all relevant python versions. To see which versions are required, see tox.ini *envlist*. 

Install a required version, e.g.: `pyenv install 3.9.0`

Set versions locally for the project (or globally if desired): `pyenv local 3.9.0 3.8.6`

Install tox: 
`pip install tox`

To install dependencies and run tests, run `tox`. 
Running `tox -r` will recreate all virtualenvs.
