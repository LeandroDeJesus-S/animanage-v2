from collections.abc import Iterable, Iterator
from abc import abstractmethod, abstractproperty


class IAnime(Iterable):
    @property
    @abstractmethod
    def as_dict(self) -> dict:
        ...
    
    @property
    @abstractmethod
    def id(self) -> int:
        ...
    
    @property
    @abstractmethod
    def name(self) -> str:
        ...
    
    @property
    @abstractmethod
    def sinopse(self) -> str: 
        ...
    
    @property
    @abstractmethod
    def url(self) -> str:
        ...
    
    @property
    @abstractmethod
    def year(self) -> str:
        ...
    
    @property
    @abstractmethod
    def rate(self) -> float:
        ...