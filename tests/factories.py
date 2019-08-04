import tempfile
import pathlib

TEST_MOVIES = ["Jumanji.Welcome.to.the.Jungle.2017.480p.BluRay.x264.mkv",
               "Jumanji.Welcome.to.the.Jungle.480p.BluRay.x264.mkv",
              ]


class movie_file:
    """Dirty hack to bypass weakref from TemporaryDirectory and stay DRY."""

    def __new__(cls, movie_file):
        cls.tempdir = tempfile.TemporaryDirectory()
        path = cls.tempdir
        temp_movie = pathlib.Path(path.name) / movie_file
        return temp_movie
