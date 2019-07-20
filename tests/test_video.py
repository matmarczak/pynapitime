import pathlib
import tempfile
from unittest import TestCase, mock
from .factories import movie_file
from utils.video import Video

def file_mocker(func):
    video_track_mock = mock.Mock()
    video_track_mock.duration.side_effect = 123
    video_track_mock.frame_rate.side_effect = '24'
    @mock.patch('utils.video.Video._extract_video_track', video_track_mock)
    def decorate_function(cls):
        return func(cls)
    return decorate_function

class VideoTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_movie = movie_file()
        cls.video = Video(cls.temp_movie)

    def test_video_saves_path(self):
        self.assertIsInstance(self.video.path, pathlib.Path)
        self.assertEqual(self.video.path.__str__(), str(self.temp_movie))

    def test_check_for_subs_doesnt_exists(self):
        subs_path = self.video.path.with_suffix('.mkv.txt')
        if subs_path.exists():
            # ensure path is clean
            subs_path.unlink()
        self.video.subs_exist()
        self.assertFalse(self.video.subtitles_exist)

    def test_check_if_existing_subtitles_are_handles(self):
        subs_path = self.video.path.with_suffix('.mkv.txt')
        subs_path.touch()
        with subs_path.open('w') as file:
            file.write('tests subs')
        self.assertEqual(subs_path, self.video.path.with_suffix('.mkv.txt'))
        self.assertTrue(subs_path.exists())
        self.video.subs_exist()
        self.assertTrue(self.video.subtitles_exist)

    @file_mocker
    def test_get_track_data(self):
            self.video.get_track_data()
            self.assertTrue(self.video.duration)
            self.assertTrue(self.video.frame_rate)

    def test_get_name(self):
        self.video.parse_name()
        self.assertEqual(self.video.title, 'Jumanji Welcome to the Jungle')
        self.assertEqual(self.video.year, 2017)

    @file_mocker
    def test_gather_data(self):
        self.video.collect_movie_data()
        self.assertTrue(self.video.duration)
        self.assertTrue(self.video.frame_rate)
        self.assertTrue(self.video.title)
        self.assertTrue(self.video.year)
