from unittest import TestCase
from pynapitime.video import Video
from pynapitime.browser import Browser
from test.config import TEST_FILE_PATH


class TestBrowser(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.video = Video(TEST_FILE_PATH)
        cls.video.collect_movie_data()
        cls.browser = Browser(cls.video)

    def test_movie_list(self):
        movie_list = self.browser.get_movies_list()
        self.assertIsInstance(movie_list, list)

    def test_find_movie(self):
        movie = self.browser.find_movie()
        self.assertIsInstance(movie, dict)
        self.assertTrue(movie['title'])

    def test_get_subtitles_list(self):
        subs_list = self.browser.get_subtitles_list()
        self.assertTrue(len(subs_list)>0)
