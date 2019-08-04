import pathlib
import tempfile
from unittest import TestCase, mock
from .factories import movie_file, TEST_MOVIES
from utils.video import Video


def file_mocker(func):
    video_track_mock = mock.Mock(duration=2134, frame_rate='24')

    return_mock = mock.Mock()
    return_mock.return_value = video_track_mock

    @mock.patch("utils.video.Video._extract_video_track", return_mock)
    def decorate_function(cls):
        return func(cls)

    return decorate_function


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

    def test_get_name(self):
        self.video.parse_name()
        self.assertEqual(self.video.title, "Jumanji Welcome to the Jungle")
        self.assertEqual(self.video.year, 2017)

    @file_mocker
    def test_gather_data(self):
        self.video.collect_movie_data()
        self.assertTrue(self.video.duration)
        self.assertTrue(self.video.frame_rate)
        self.assertTrue(self.video.title)
        self.assertTrue(self.video.year)

# allows parametrizing test cases in unittest
for idx, i in enumerate(TEST_MOVIES):
    globals()['TestVideo{}'.format(idx)] = type('VideoTest', (VideoTest, TestCase), {'test_movie_file':TEST_MOVIES[idx]})
