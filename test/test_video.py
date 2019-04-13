from unittest import TestCase
from pynapitime.video import Video
import pathlib
from test.config import TEST_FILE_PATH
import time

class VideoTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = TEST_FILE_PATH
        cls.video = Video(cls.path)

    def test_video_saves_path(self):
        self.assertIsInstance(self.video._path, pathlib.Path)
        self.assertEqual(self.video._path.__str__(), self.path)

    def test_check_for_subs(self):
        subs_path = self.video._path.with_suffix('.mkv.txt')
        if subs_path.exists():
            #ensure path is clean
            subs_path.unlink()
        self.video.check_for_subs()
        self.assertFalse(self.video.subtitles_exist)

        subs_path.touch()
        with subs_path.open('w') as file:
            file.write('test subs')

        self.assertEqual(subs_path, self.video._path.with_suffix('.mkv.txt'))
        self.assertTrue(subs_path.exists())
        self.video.check_for_subs()
        self.assertTrue(self.video.subtitles_exist)
        subs_path.unlink()

    def test_get_track_data(self):
        duration = self.video.get_track_data()
        self.assertTrue(self.video.duration)
        self.assertTrue(self.video.frame_rate)

    def test_get_name(self):
        self.video.parse_name()
        self.assertTrue(self.video.title)
        self.assertTrue(self.video.year)

    def test_gather_data(self):
        self.video.collect_movie_data()
        self.assertTrue(self.video.duration)
        self.assertTrue(self.video.frame_rate)
        self.assertTrue(self.video.title)
        self.assertTrue(self.video.year)



