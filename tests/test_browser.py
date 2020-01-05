import pytest

from src import browser
from src.browser import Browser


def test_found_movies(mock_videoclip, browser):
    movie = browser._get_movie()
    assert isinstance(movie, dict)
    assert movie["title"]
    assert movie["year"]
    assert movie["href"]


def test_get_subtitles_list(mock_videoclip, browser):
    subs = browser.get_subtitles_list()
    assert subs


@pytest.mark.parametrize(
    "timestr,expected_ms",
    [
        ("00:21:54.800", 800+54*1000+21*60*1000),
        ("00:25:00.960", 1500960.0)
    ]
)
def test_time_to_ms(timestr, expected_ms):
    converted_time = browser.time_to_ms(timestr)
    assert converted_time == expected_ms


@pytest.mark.parametrize(
    "fps_str,expected",
    [
        ("FPS: </b> 25 <asdf>", 25),
        ("FPS: </b> 23.967823421 <asdf>", 23.97),
        ("FPS: </b> 24 <asdf>", 24)
    ]
)
def test_fps_field_clean(fps_str, expected):
    assert Browser._clean_fps(fps_str) == expected