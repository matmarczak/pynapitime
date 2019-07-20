from unittest import TestCase, mock
from utils.video import Video
from utils.browser import Browser
import tempfile
import pathlib
import shutil
from .test_video import file_mocker

class TestBrowser(TestCase):

    @classmethod
    def setUp(cls):
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.path = cls.tempdir
        cls.temp_movie = pathlib.Path(cls.path.name) / "Jumanji.Welcome.to.the.Jungle.2017.480p.BluRay.x264.mkv"
        cls.video = Video(cls.temp_movie)
        cls.video.parse_name()
        cls.video.duration = 7143143
        cls.browser = Browser(cls.video)

    def test_movie_list(self):
        movie_list = self.browser.get_movies_list()
        self.assertIsInstance(movie_list, list)

    @file_mocker
    def test_find_movie(self):
        self.video.collect_movie_data()
        movie = self.browser.find_movie()
        self.assertIsInstance(movie, dict)
        self.assertTrue(movie['title'])

    @file_mocker
    def test_get_subtitles_list(self):
            subs_list = self.browser.get_subtitles_list()
            self.assertTrue(len(subs_list) > 0)
