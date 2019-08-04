import tempfile
import pathlib
from unittest import mock
TEST_MOVIES = ["Jumanji.Welcome.to.the.Jungle.2017.480p.BluRay.x264.mkv",
               "Jumanji.Welcome.to.the.Jungle.480p.BluRay.x264.mkv",
              ]


def file_mocker(func):
    video_track_mock = mock.Mock(duration=2134, frame_rate='24')

    return_mock = mock.Mock()
    return_mock.return_value = video_track_mock

    @mock.patch("utils.video.Video._extract_video_track", return_mock)
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
