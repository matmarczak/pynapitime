from typing import NamedTuple
from unittest.mock import Mock, patch

import pytest
import vcr

from src.browser import Browser
from src.video import Video

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
def browser(video):
    return Browser(video)


@pytest.fixture
def track_data():
    mock_extract = Mock(return_value=(2134, 23.97))
    with patch("src.video.Video._extract_video_track", mock_extract):
        yield


vcr_mocks = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="tests/response_mocks",
    record_mode="once",
    match_on=("method", "scheme", "host", "port", "path", "query", "body"),
    decode_compressed_response=True,
)


@pytest.fixture(autouse=True, scope="session")
def response_mocks():
    with vcr_mocks.use_cassette("napiprojekt_mocks.yml"):
        yield


@pytest.fixture
def mock_videoclip():
    with patch(
            "src.video.VideoFileClip",
            return_value=Mock(duration=(23 * 60 + 30), fps=24)
    ) as mock_video:
        yield mock_video
