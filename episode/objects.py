from __future__ import annotations
from collections.abc import Iterable, Iterator
from anime.interfaces import IAnime
from .interfaces import IEpisode
from typing import Any, List, Dict, Any, Union
from pprint import pprint
import re
import io
import operator


class Episode(IEpisode):
    def __init__(self, ep: dict[str, Any]) -> None:
        self._ep = ep
        self._valid_keys = [
            'id',
            'anime_id',
            'season',
            'num',
            'url'
        ]
        self.regex_validations = {
            'id': lambda x: re.match(r'\d', x),
            'anime_id': lambda x: re.match(r'\d', x),
            'season': lambda x: re.match(r'\d', x),
            'num': lambda x: re.match(r'\d', x),
            'url': lambda x: re.match(r'https\:\/\/animesonlinecc.to\/episodio\/[\w\d-]+\-episodio\-\d+\/', x),
        }
        self._keys = list(ep.keys())
        self.__validate_keys()
        self.__validate_item_type(Union[int, str])
        self.__validate_item_values()
    
    @property
    def as_dict(self) -> dict:
        return self._ep
    
    def __validate_item_type(self, type) -> None:
        for item, value in self._ep.items():
            assert isinstance(value, type), f'{item} type must be in {type}'
    
    def __validate_item_values(self) -> None:
        for k, v in self._ep.items():
            res = self.regex_validations[k](str(v))
            assert not res is None, f'reg is None for {k} = {v}'
    
    def __validate_keys(self):
        if not hasattr(self, '_valid_keys'):
            raise AttributeError('_valid_keys argument not found')
        
        elif not hasattr(self, '_keys'):
            raise AttributeError('_keys argument not found')
        
        assert sorted(self._keys) == sorted(self._valid_keys), f'{self._keys} != {self._valid_keys}'
    
    @property
    def id(self):
        return self._ep['id']

    @property
    def anime_id(self):
        return self._ep['anime_id']
    
    @property
    def season(self):
        return self._ep['season']
    
    @property
    def number(self):
        return self._ep['num']
    
    @property
    def url(self):
        return self._ep['url']
    
    def __iter__(self) -> Iterator:
        return iter(self._ep)
    
    def __next__(self) -> Any:
        return next(self.__iter__())
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        args = ', '.join([f'{k}:{type(v).__name__}={v}' for k, v in self._ep.items()])
        return f'{self.__class__.__name__}({args})'
    
    def __eq__(self, __value: IAnime|Episode) -> bool:
        if isinstance(__value, IAnime):
            return self.anime_id == __value.id
        
        elif isinstance(__value, Episode):
            return self.id == __value.id
        
        else:
            raise TypeError(
                f'only supports operator = with objects of type {self.__class__} or {self.__class__.__name__}'
            )
    
    def __ne__(self, __value: IAnime|Episode) -> bool:
        return not self.__eq__(__value)
    
    def __gt__(self, __value: Episode) -> bool:
        if not isinstance(__value, Episode):
            raise TypeError(f'{__value.__qualname__} must be type {self.__class__.__name__}')
        
        if self.season > __value.season:
            return True
        
        elif self.season == __value.season and self.number > __value.number:
            return True
        
        return False
    
    def __lt__(self, __value: Episode) -> bool:
        return not self.__gt__(__value)


class Episodes(Iterator):
    def __init__(self, eps: List[Dict]) -> None:
        self._eps = [Episode(e) for e in eps]
    
    def __iter__(self) -> Iterator:
        return iter(self._eps)
    
    def __next__(self):
        return next(self.__iter__())
    
    def __getitem__(self, slice):
        return self._eps[slice]
    
    def __len__(self):
        return len(self._eps)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        stream = io.StringIO()
        pprint(self._eps, stream=stream, indent=4)
        out = stream.getvalue()
        stream.close()
        return out
    
    @staticmethod
    def __bin_search(anime: IAnime, eps: Episodes):
        low = 0
        high = len(eps) - 1
        mid = 0

        while low <= high:
            mid = (high + low) // 2

            if eps[mid].anime_id < anime.id:
                low = mid + 1

            elif eps[mid].anime_id > anime.id:
                high = mid - 1

            else:
                return mid

        return -1

    @classmethod
    def find_all_indices(cls, arr: Episodes, target: IAnime):
        arr = sorted(arr, key=lambda a: a.anime_id)  # type: ignore
        index = cls.__bin_search(target, arr)
        if index == -1:
            return []
        
        indexes = [index]
        
        i = index - 1
        while i >= 0 and arr[i] == target:
            indexes.append(i)
            i -= 1
        
        i = index + 1
        while i < len(arr) and arr[i] == target:
            indexes.append(i)
            i += 1
        
        return sorted(indexes)


    
    @classmethod
    def from_anime(cls, anime: IAnime, eps: List[Dict]):
        instance = cls(eps)
        idxs = cls.find_all_indices(instance, anime)
        eps = [instance[i] for i in idxs]
        return eps


# if __name__ == '__main__':
#     import random
#     a = [
#         {
#             'id': 1,
#             'name': 'anime test',
#             'url': 'https://animesonlinecc.to/anime/bocchi-the-rock/',
#             'sinopse': 'A história acompanha Hitori Gotou, uma garota sem \
#                 amigos que está aprendendo a tocar guitarra para se tornar \
#                 uma estrela do rock, mas é extremamente tímida. Por mais \
#                 que seu sonho parecesse inalcançável, ela acaba por conhecer\
#                  Nijika Ijichi, uma baterista que está a procura de uma guitarrista\
#                  para sua banda, criando assim a oportunidade para HItori entrar no mundo da música.',
#             'year': '2024',
#             'rate': 9.5
#         } for i in range(100)
#     ]
#     es = [
#         {
#             'id': 1,
#             'anime_id': 1, 
#             'season': 2,
#             'num': 1,
#             'url': 'https://animesonlinecc.to/episodio/boku-no-hero-academia-2-episodio-1/'
#         } for i in range(5)
#     ]
    
#     anm = Animes(a)
#     anm = anm.filter('name', 'test', operator.contains)
#     print(anm, '\n')
#     anm = anm.first()
#     if anm is not None:
#         eps = Episodes.from_anime(anm, es)
#         pprint(eps)
#         # ae = AnimeEp(anm, eps)
    
#     else:
#         print('anime não encontrado.')
