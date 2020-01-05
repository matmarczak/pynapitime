import pathlib
from src.video import Video


class TestSeriesEpisodes:
    def test_series_are_detected(self, series_episode):
        test_video = Video(series_episode)
        test_video.parse_name()
        assert test_video.title
        assert test_video.year
        assert test_video.episode
        assert test_video.season


class TestVideo:
    def test_video_saves_path(self, video, movie_path):
        assert isinstance(video.path, pathlib.Path)
        assert video.path.__str__() == str(movie_path)

    def test_check_for_subs_doesnt_exists(self, video):
        subs_path = video.path.with_suffix(".mkv.txt")
        if subs_path.exists():
            # ensure path is clean
            subs_path.unlink()
        video.subs_exist()
        assert not video.subtitles_exist

    def test_check_if_existing_subtitles_are_handles(self, video):
        subs_path = video.path.with_suffix(".mkv.txt")
        subs_path.touch()
        with subs_path.open("w") as file:
            file.write("tests subs")
        assert subs_path == video.path.with_suffix(".mkv.txt")
        assert subs_path.exists()
        assert video.subs_exist()
        assert video.subtitles_exist

    def test_get_track_data(self, track_data, video):
        video.get_track_data()
        assert isinstance(video.duration, int)
        assert isinstance(video.frame_rate, float)

    def test_results_tuples(self, video, track_data):
        video.collect_movie_data()
        isinstance(video.duration, int)
        isinstance(video.frame_rate, str)
        isinstance(video.title, str)
        isinstance(video.year, (int, type(None)))

    def test_get_name(self, video, movie):
        video.parse_name()
        assert video.title == movie.title
        assert video.year == movie.year

    def test_gather_data(self, video, track_data):
        video.collect_movie_data()
        assert video.duration == 2134
        assert video.frame_rate == 23.97
