import string
import tempfile
import pathlib
import random
from unittest import mock

TEST_MOVIES = [
    "Jumanji.Welcome.to.the.Jungle.2017.480p.BluRay.x264.mkv",
    "Jumanji.Welcome.to.the.Jungle.480p.BluRay.x264.mkv",
]


def file_mocker(func):
    video_track_mock = mock.Mock(duration=2134, frame_rate="23.97")

    return_mock = mock.Mock()
    return_mock.return_value = video_track_mock

    @mock.patch("src.video.Video._extract_video_track", return_mock)
    def decorate_function(cls):
        return func(cls)

    return decorate_function


class movie_file:
    """Dirty hack to bypass weakref from TemporaryDirectory and stay DRY."""

    def __new__(cls, movie_file):
        cls.tempdir = tempfile.TemporaryDirectory()
        path = cls.tempdir
        temp_movie = pathlib.Path(path.name) / movie_file
        return temp_movie


def random_movie_string(len=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(len)) + ".mkv"


class MovieFilesFactory:
    def __init__(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.movies = {}
        for i in range(10):
            movie = pathlib.Path(self.tempdir.name) / random_movie_string()
            movie.touch()
            self.movies[i] = movie
