from dataclasses import dataclass
from enum import Enum

_tv_file_output_pattern = '{name} - s{season}e{episode} - {episode_name}.{extension}'


@dataclass
class TvMediaItem:
    name: str
    season_number: str
    episode_number: str
    file_extension: str
    original_filename: str
    episode_name: str = None

    def get_episode_number(self) -> str:
        return self.episode_number

    def filename(self) -> str:
        return _tv_file_output_pattern \
            .format(name=self.name, season=self.season_number, episode=self.episode_number,
                    episode_name=self.episode_name, extension=self.file_extension)


class MediaType(Enum):
    tv = 'tv'
    movie = 'movie'
