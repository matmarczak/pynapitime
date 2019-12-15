import pytest

series_episodes = [
    "Friends.S01E09.1994.super.mkv",
    "Friends.S01E07.1994.super.mkv",
    "Friends.S01E08.1994.super.mkv",
]

@pytest.fixture(params=series_episodes)
def series_episode(request):
    return request.param
