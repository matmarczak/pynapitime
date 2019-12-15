import pathlib
from unittest import TestCase

from .factories import movie_file, file_mocker, TEST_MOVIES
from utils.video import Video


class VideoTest:
    @classmethod
    def setUpClass(cls):
        cls.temp_movie = movie_file(cls.test_movie_file)
        cls.video = Video(cls.temp_movie)

    def test_video_saves_path(self):
        self.assertIsInstance(self.video.path, pathlib.Path)
        self.assertEqual(self.video.path.__str__(), str(self.temp_movie))

    def test_check_for_subs_doesnt_exists(self):
        subs_path = self.video.path.with_suffix(".mkv.txt")
        if subs_path.exists():
            # ensure path is clean
            subs_path.unlink()
        self.video.subs_exist()
        self.assertFalse(self.video.subtitles_exist)

    def test_check_if_existing_subtitles_are_handles(self):
        subs_path = self.video.path.with_suffix(".mkv.txt")
        subs_path.touch()
        with subs_path.open("w") as file:
            file.write("tests subs")
        self.assertEqual(subs_path, self.video.path.with_suffix(".mkv.txt"))
        self.assertTrue(subs_path.exists())
        self.video.subs_exist()
        self.assertTrue(self.video.subtitles_exist)

    @file_mocker
    def test_get_track_data(self):
        self.video.get_track_data()
        self.assertIsInstance(self.video.duration, int)
        self.assertIsInstance(self.video.frame_rate, str)

    @file_mocker
    def test_results_tupes(self):
        self.video.collect_movie_data()
        self.assertIsInstance(self.video.duration, int)
        self.assertIsInstance(self.video.frame_rate, str)
        self.assertIsInstance(self.video.title, str)
        self.assertIsInstance(self.video.year, (int, type(None)))


class TestVideo_1(VideoTest, TestCase):
    test_movie_file = TEST_MOVIES[0]

    def test_get_name(self):
        self.video.parse_name()
        self.assertEqual(self.video.title, "Jumanji Welcome to the Jungle")
        self.assertEqual(self.video.year, 2017)

    @file_mocker
    def test_gather_data(self):
        self.video.collect_movie_data()
        self.assertEqual(self.video.duration, 2134)
        self.assertEqual(self.video.frame_rate, "24")


class TestVideo_2(VideoTest, TestCase):
    test_movie_file = TEST_MOVIES[1]

    def test_get_name(self):
        self.video.parse_name()
        self.assertEqual(self.video.title, "Jumanji Welcome to the Jungle")
        self.assertEqual(self.video.year, None)

    @file_mocker
    def test_gather_data(self):
        self.video.collect_movie_data()
        self.assertEqual(self.video.duration, 2134)
        self.assertEqual(self.video.frame_rate, "24")


class TestSeriesEpisodes:
    def test_series_are_detected(self, series_episode):
        test_video = Video(series_episode)
        test_video.parse_name()
        assert test_video.title
        assert test_video.year
        assert test_video.episode
        assert test_video.season
        assert test_video.episode == "09"
        assert test_video.season == "01"
