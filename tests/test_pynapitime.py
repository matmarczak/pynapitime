from tests.factories import movie_file, TEST_MOVIES
from pynapitime import handle_file, main
import unittest
from unittest.mock import Mock, patch
from utils.exceptions import BadFile
from tests.test_video import file_mocker


class TestPynapitime(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.temp_movie = movie_file(TEST_MOVIES[0])
        cls.temp_movie.touch()

    @file_mocker
    def test_handle_file(self):
        handle_file(self.temp_movie, Mock(match=0))
