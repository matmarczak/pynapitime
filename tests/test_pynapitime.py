from tests.factories import movie_file, TEST_MOVIES
from pynapitime import handle_file
import unittest
from unittest.mock import Mock
from utils.exceptions import BadFile
from tests.test_video import file_mocker


class TestPynapitime(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.temp_movie = movie_file(TEST_MOVIES[0])
        cls.temp_movie.touch()

    def test_handle_file_raises_exc_on_bad_file(self):
        with self.assertRaises(BadFile):
            handle_file(self.temp_movie, Mock(match=0))

    @file_mocker
    def test_handle_file(self):
        handle_file(self.temp_movie, Mock(match=0))
