from typing import NamedTuple
from unittest.mock import Mock, patch

import pytest

from utils.video import Video

series_episodes = [
    "Friends.S01E09.1994.super.mkv",
    "Friends.S01E07.1994.super.mkv",
    "Friends.S01E08.1994.super.mkv",
]


@pytest.fixture(params=series_episodes)
def series_episode(request):
    return request.param


class TestMovie(NamedTuple):
    filename: str
    title: str
    year: int


test_movies = [
    TestMovie(
        "Jumanji.Welcome.to.the.Jungle.2017.480p.BluRay.x264.mkv",
        "Jumanji Welcome to the Jungle",
        2017
    ),
    TestMovie(
        "Jumanji.Welcome.to.the.Jungle.480p.BluRay.x264.mkv",
        "Jumanji Welcome to the Jungle",
        None
    )
]
@pytest.fixture(params=test_movies)
def movie(request):
    return request.param


@pytest.fixture
def movie_path(movie, tmpdir):
    return tmpdir.join(movie.filename)


@pytest.fixture
def video(movie_path):
    return Video(movie_path)


@pytest.fixture
def track_data():
    mock_extract = Mock(return_value=(2134, "24"))
    with patch("utils.video.Video._extract_video_track", mock_extract):
        yield
