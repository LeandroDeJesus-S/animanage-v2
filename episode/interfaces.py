from collections.abc import Iterable
from abc import abstractmethod


class IEpisode(Iterable):
    @property
    @abstractmethod
    def id(self) -> int:
        ...

    @property
    @abstractmethod
    def anime_id(self) -> int:
        ...
    
    @property
    @abstractmethod
    def season(self) -> int:
        ...
    
    @property
    @abstractmethod
    def number(self) -> int:
        ...
    
    @property
    @abstractmethod
    def url(self) -> str:
        ...
    
