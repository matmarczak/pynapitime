from tests.factories import movie_file
from pynapitime import handle_file
import unittest
from unittest.mock import patch, Mock
from utils.exceptions import BadFile
from tests.test_video import file_mocker

class TestPynapitime(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.temp_movie = movie_file()
        cls.temp_movie.touch()

    def test_handle_file_raises_exc_on_bad_file(self):
        with self.assertRaises(BadFile):
            handle_file(self.temp_movie)

    @file_mocker
    def test_handle_file(self):
        # TODO
        # Mocks video duration to allow program handling movie subtitiles
        # from Browser, read about unittest.mock to mock duration of video
        with patch('utils.video.Video') as mock:
            duration = Mock()
            duration.side_effect = 123
            mock.duration = duration
            handle_file(self.temp_movie)
