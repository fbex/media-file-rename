# media-file-rename

A script to detect media files inside a given directory and rename them by a certain pattern.
Media files are enriched with information from TMDB.

Note that the script currently only supports TV shows. 

## How to run

Requires a TMDB api key in environment variable like this: `export TMDB_API_KEY=<api-key>`.
To get an API key, simply register an account at https://www.themoviedb.org.

Run with: `python3 -m media-file-rename`
