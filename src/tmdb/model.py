from dataclasses import dataclass

from common.model import MediaType


@dataclass
class TmdbItem:
    id: int
    name: str
    type: MediaType


@dataclass
class TvEpisode:
    number: int
    name: str
