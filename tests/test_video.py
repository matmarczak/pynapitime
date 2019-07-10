import pathlib
import tempfile
from unittest import TestCase, mock

from pynapitime.video import Video


class VideoTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.path = cls.tempdir
        cls.video = Video(cls.path.name + '.mkv ')

    @classmethod
    def tearDownClass(cls):
        cls.tempdir.cleanup()

    def test_video_saves_path(self):
        self.assertIsInstance(self.video.path, pathlib.Path)
        self.assertEqual(self.video.path.__str__(), self.path)

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

    def test_get_track_data(self):
        mediainfo_mock = mock.Mock()
        mocked_mediafile = mock.Mock()
        mocked_mediafile.tracks.side_effect = [123]
        mediainfo_mock.parse.side_effect = mocked_mediafile
        with mock.patch('pynapitime.video.MediaInfo', mediainfo_mock):
            self.video.get_track_data()
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
