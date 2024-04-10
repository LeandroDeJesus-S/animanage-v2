from __future__ import annotations
from collections.abc import Iterable, Iterator
from typing import Any, NewType, List, Dict, Sequence, Any, Union
from pprint import pprint
from .interfaces import IAnime
from episode.interfaces import IEpisode
import re
import io


class Anime(IAnime):
    def __init__(self, item: Dict[str, Any]) -> None:
        self.item = item
        self._item_keys = list(self.item.keys())
        self._item_valid_keys = ['id', 'name', 'sinopse', 'url', 'year', 'rate']

        self.regex_validations = {
            'id': lambda x: re.match(r'\d', x),
            'name': lambda x: re.match(r'[\w+\s*\d*]', x, re.I),
            'sinopse': lambda x: re.match(r'[\w+\s*\d*]', x, re.I),
            'url': lambda x: re.match(r'https\:\/\/animesonlinecc.to\/anime\/[\w-]+\/', x),
            'year': lambda x: re.match(r'^[12]\d{3}', x),
            'rate': lambda x: re.match(r'\d+\.\d+', x)
        }

        self.__validate_item_keys(self._item_keys, self._item_valid_keys)
        self.__validate_item_type(Union[str, int, float])
        self.__validate_item_values(self.item)
    
    def __bsearch(self, x, arr):
        low = 0
        high = len(arr) - 1
        mid = 0

        while low <= high:

            mid = (high + low) // 2

            if arr[mid] < x:
                low = mid + 1

            elif arr[mid] > x:
                high = mid - 1

            else:
                return mid

        return -1

    @property
    def as_dict(self) -> dict:
        return self.item
    
    @property
    def id(self) -> int:
        return self.item['id']
    
    @property
    def name(self) -> str:
        return self.item['name']
    
    @property
    def sinopse(self) -> str: 
        return self.item['sinopse']
    
    @property
    def url(self) -> str:
        return self.item['url']
    
    @property
    def year(self) -> str:
        return self.item['year']
    
    @property
    def rate(self) -> float:
        return self.item['rate']
    
    def __next__(self) -> Any:
        return next(self.__iter__())
    
    def __iter__(self) -> Iterator:
        return iter(self.item)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        args = ', '.join([f'{k}:{type(v).__name__}={v}' for k, v in self.item.items()])
        return f'{self.__class__.__name__}({args})'
    
    def __eq__(self, __value: Anime|IEpisode) -> bool:
        if isinstance(__value, Anime):
            return self.id == __value.id
        
        elif isinstance(__value, IEpisode):
            return self.id == __value.anime_id
        
        else:
            raise TypeError(
                f'only supports operator = with objects of type {self.__class__} or {IEpisode.__class__}'
            )
    
    def __ne__(self, __value: Anime) -> bool:
        return not self.__eq__(__value)

    @staticmethod
    def __validate_item_keys(_valid_keys, _item_keys) -> None:
        vk_sorted = sorted(_valid_keys)
        ik_sorted = sorted(_item_keys)
        assert vk_sorted == ik_sorted, f'{vk_sorted} != {ik_sorted}'

    def __validate_item_type(self, type) -> None:
        for item, value in self.item.items():
            assert isinstance(value, type), f'{item} type must be in {type}'
    
    def __validate_item_values(self, item: dict) -> None:
        for k, v in item.items():
            res = self.regex_validations[k](str(v))
            assert not res is None


class Animes(Iterable):
    def __init__(self, animes: list[dict]) -> None:
        self._animes = [Anime(a) for a in animes]

    def filter(self, attr, value, operation) -> Animes:
        f = [
            a.as_dict
            for a in filter(
                lambda a: operation(getattr(a, attr), value), self._animes
            )
        ]
        return Animes(f)
        
    def first(self) -> Anime|None:
        return self._animes[0] if len(self._animes) > 0 else None
    
    def as_generator(self):
        for anime in self._animes:
            yield anime

    def __next__(self) -> Anime:
        return next(self.__iter__())
    
    def __iter__(self) -> Iterator:
        return iter(self._animes)
    
    def __getitem__(self, slice) -> list[Anime]|Anime:
        return self._animes[slice]
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        stream = io.StringIO()
        pprint(self._animes, stream=stream, indent=4)
        out = stream.getvalue()
        stream.close()
        return out
