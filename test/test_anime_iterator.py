from unittest import TestCase
from episode.objects import Episode
from anime.objects import Anime


class TestAnime(TestCase):
    def setUp(self) -> None:
        self.valid_sample = {
            'id': 1,
            'name': 'anime test',
            'url': 'https://animesonlinecc.to/anime/bocchi-the-rock/',
            'sinopse': 'A história acompanha Hitori Gotou, uma garota sem \
                amigos que está aprendendo a tocar guitarra para se tornar \
                uma estrela do rock, mas é extremamente tímida. Por mais \
                que seu sonho parecesse inalcançável, ela acaba por conhecer\
                 Nijika Ijichi, uma baterista que está a procura de uma guitarrista\
                 para sua banda, criando assim a oportunidade para HItori entrar no mundo da música.',
            'year': '2024',
            'rate': 9.5
        }
    
    def test_anime_raise_assertion_error_with_invlid_keys(self):
        with self.assertRaises(AssertionError):
            invalid = self.valid_sample.copy()
            invalid['invalid_key'] = 0
            anime = Anime(invalid)
    
    def test_anime_no_raises_with_valid_keys(self):
        anime = Anime(self.valid_sample)
        self.assertIsInstance(anime, Anime)
    
    def test_anime_raises_with_invalid_type(self):
        with self.assertRaises(AssertionError):
            invalid = self.valid_sample.copy()
            invalid['rate'] = [0]
            anime = Anime(invalid)
        
    def test_regex_validators_raises_with_invalid_entry_value(self):
        invalid = self.valid_sample.copy()
        invalid['url'] = 'http://animesonline.cc/anime/inv@lido/'
        with self.assertRaises(AssertionError):
            anime = Anime(invalid)
    
    def test_as_dict_return_instance_of_dict(self):
        anime = Anime(self.valid_sample)
        self.assertIsInstance(anime.as_dict, dict)
    
    def test_anime_raise_if_not_compared_with_Anime_or_Episode_obj(self):
        anime1 = Anime(self.valid_sample)
        anime2 = Anime(self.valid_sample.copy())
        ep = Episode({
            'id': 1,
            'anime_id': anime1.id,
            'num': 1,
            'url': 'https://animesonlinecc.to/episodio/boku-no-hero-academia-2-episodio-1/',
            'season': 2
        })
        with self.subTest(anime1=anime1, anime2=anime2):
            self.assertEqual(anime1, anime2)

        with self.subTest(anime1=anime1, ep=ep):
            self.assertEqual(anime1, ep)
        
        with self.subTest(anime1=anime1, anime2=self.valid_sample):
            with self.assertRaises(TypeError):
                self.assertEqual(anime1, self.valid_sample)
    
    def test_properties_return_types(self):
        anime = Anime(self.valid_sample)
        cases = [
            (anime.id, int),
            (anime.name, str),
            (anime.url, str),
            (anime.rate, float),
            (anime.sinopse, str),
            (anime.year, str)
        ]
        for case in cases:
            ppt, typ = case
            with self.subTest(property=ppt, type=typ):
                self.assertIsInstance(ppt, typ)



