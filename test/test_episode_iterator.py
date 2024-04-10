from unittest import TestCase
from episode.objects import Episode
from anime.objects import Anime


class TestEpisode(TestCase):
    def setUp(self) -> None:
        self.valid_sample = {
            'id': 1,
            'anime_id': 1, 
            'season': 2,
            'num': 1,
            'url': 'https://animesonlinecc.to/episodio/boku-no-hero-academia-2-episodio-1/'
        }
    
    def test_eq_and_lt_operator_with_another_ep_obj(self):
        ep0 = Episode({
            'id': 1,
            'anime_id': 1, 
            'season': 1,
            'num': 1,
            'url': 'https://animesonlinecc.to/episodio/boku-no-hero-academia-2-episodio-1/'
        })
        ep1 = Episode({
            'id': 1,
            'anime_id': 1, 
            'season': 2,
            'num': 1,
            'url': 'https://animesonlinecc.to/episodio/boku-no-hero-academia-2-episodio-1/'
        })
        ep2 = Episode({
            'id': 1,
            'anime_id': 1, 
            'season': 2,
            'num': 2,
            'url': 'https://animesonlinecc.to/episodio/boku-no-hero-academia-2-episodio-1/'
        })

        test1 = ep0 > ep1
        expected1 = False
        self.assertEqual(test1, expected1)

        test2 = ep1 > ep0
        expected2 = True
        self.assertEqual(test2, expected2)

        test3 = ep2 > ep0 and ep2 > ep1
        expected3 = True
        self.assertEqual(test3, expected3)

        test4 = ep0 < ep1
        expected4 = True
        self.assertEqual(test4, expected4)

        test5 = ep1 < ep0
        expected5 = False
        self.assertEqual(test5, expected5)

        test6 = ep2 < ep0 and ep2 < ep1
        expected6 = False
        self.assertEqual(test6, expected6)
   
    def test_instance_with_valid_entries(self):
        ep = Episode(self.valid_sample)
        self.assertIsInstance(ep, Episode)
    
    def test_regex_validations_with_invalid_url(self):
        invalid_url = self.valid_sample.copy()
        invalid_url['url'] = 'https://animesonlinecc.to/episodio/boku-no-hero-academia-2/'
        with self.assertRaises(AssertionError):
            ep = Episode(invalid_url)
    
    def test_instace_with_invalid_key(self):
        invalid = self.valid_sample.copy()
        invalid['invalid key'] = 'invalid'
        with self.assertRaises(AssertionError):
            ep = Episode(invalid)
        
    def test_properties_return_types(self):
        ep = Episode(self.valid_sample)
        cases = [
            (ep.id, int),
            (ep.anime_id, int),
            (ep.season, int),
            (ep.number, int),
            (ep.url, str),
        ]
        for case in cases:
            ppt, typ = case
            with self.subTest(property=ppt, type=typ):
                self.assertIsInstance(ppt, typ)

    def test_ep_raise_if_not_compared_with_Anime_or_Episode_obj(self):
        ep1 = Episode(self.valid_sample)
        ep2 = Episode(self.valid_sample.copy())
        anime = Anime({
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
        })
        with self.subTest(ep1=ep1, ep2=ep2):
            self.assertEqual(ep1, ep2)

        with self.subTest(ep1=ep1, anime=anime):
            self.assertEqual(ep1, anime)
        
        with self.subTest(ep1=ep1, ep2=self.valid_sample):
            with self.assertRaises(TypeError):
                self.assertEqual(ep1, self.valid_sample)
    
