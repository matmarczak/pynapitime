import tempfile
import pathlib

TEST_MOVIE = "Jumanji.Welcome.to.the.Jungle.2017.480p.BluRay.x264.mkv"


class movie_file:
    """Dirty hack to bypass weakref from TemporaryDirectory and stay DRY."""

    def __new__(cls):
        cls.tempdir = tempfile.TemporaryDirectory()
        path = cls.tempdir
        temp_movie = pathlib.Path(path.name) / TEST_MOVIE
        return temp_movie
