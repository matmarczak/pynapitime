import pytest

from utils import browser


def test_found_movies(mock_videoclip, browser):
    movie = browser.find_napiprojekt_movie()
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