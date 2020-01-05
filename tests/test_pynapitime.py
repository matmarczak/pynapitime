import pytest

from pynapitime import handle_file
from unittest.mock import Mock, patch


@pytest.fixture
def mock_args():
    return Mock(match=1, title=None, year=None)


def test_handle_file(movie_path, mock_args, track_data, capsys):
    movie_path.ensure(file=True)
    handle_file(movie_path, mock_args)
    out, err = capsys.readouterr()
    assert "Found 43 subtitles" in out

def test_if_series_is_downloaded(series_episode, tmpdir, mock_args,
                                 mock_videoclip):
    with tmpdir.as_cwd():
        handle_file(series_episode, mock_args)


def test_subtitles_are_saved_when_absolute_path(series_episode, tmpdir,
                                                   mock_videoclip, mock_args):
    some_distant_file = tmpdir.join("some", "distant", "path", series_episode)
    some_distant_file.ensure()
    handle_file(some_distant_file, mock_args)
    some_distant_file.extension = "txt"
    assert some_distant_file.check(file=1)

def test_subtitles_are_saved_when_relative_path(series_episode, tmpdir,
                                                   mock_videoclip, mock_args):
    with patch("src.downloader.Path") as mock_path:
        handle_file(f"relative/path/{series_episode}", mock_args)
        assert mock_path.called
        assert mock_path.call_args[0][0].parts == ('relative', 'path', series_episode)
