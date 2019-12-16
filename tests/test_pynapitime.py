from pathlib import PosixPath

import pytest

from tests.factories import movie_file, TEST_MOVIES
from pynapitime import handle_file, main
import unittest
from unittest.mock import Mock, patch
from utils.exceptions import BadFile
from tests.test_video import file_mocker


@pytest.fixture
def mock_args():
    return Mock(match=1)

@pytest.fixture
def mock_video():
    with patch(
            "utils.video.VideoFileClip",
            return_value=Mock(duration=(23 * 60 + 30), frame_rate=24)
    ) as mock_video:
        yield mock_video

class TestPynapitime(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.temp_movie = movie_file(TEST_MOVIES[0])
        cls.temp_movie.touch()

    @file_mocker
    def test_handle_file(self, mock_args):
        handle_file(self.temp_movie)


def test_if_series_is_downloaded(series_episode, tmpdir, mock_args, mock_video):
    with tmpdir.as_cwd():
        handle_file(series_episode, mock_args)


def test_subtitles_are_saved_in_when_absolute_path(series_episode, tmpdir, mock_video, mock_args):
    some_distant_file = tmpdir.join("some", "distant", "path", series_episode)
    some_distant_file.ensure()
    handle_file(some_distant_file, mock_args)
    some_distant_file.extension = "txt"
    assert some_distant_file.check(file=1)

def test_subtitles_are_saved_in_when_relative_path(series_episode, tmpdir, mock_video, mock_args):
    with patch("utils.downloader.Path") as mock_path:
        handle_file(f"relative/path/{series_episode}", mock_args)
        assert mock_path.called
        assert mock_path.called_with(PosixPath('relative/path/{series_episode}'))
