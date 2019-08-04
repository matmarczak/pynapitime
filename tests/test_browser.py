from unittest import TestCase
from utils.video import Video
from utils.browser import Browser
from tests.factories import movie_file, file_mocker, TEST_MOVIES


class BrowserTest:
    @classmethod
    def setUp(cls):
        cls.temp_movie = movie_file(cls.test_movie_file)
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
        self.assertTrue(movie["title"])

    @file_mocker
    def test_get_subtitles_list(self):
        subs_list = self.browser.get_subtitles_list()
        self.assertTrue(len(subs_list) > 0)


for idx, i in enumerate(TEST_MOVIES):
    class_name = 'TestBrowser_{}'.format(idx)
    globals()[class_name] = type(class_name, (BrowserTest, TestCase), {'test_movie_file':i})
