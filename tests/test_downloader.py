import unittest
from tests.config import TEST_FILE_PATH
from pynapitime.video import Video
from pynapitime.downloader import Downloader


class TestDownloader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.video = Video(TEST_FILE_PATH)
        cls.test_hashes = ['34e51a07ab99cec163136ae1998363a6',
                           '74dc8c6afe25f34dcb24e591316e64d3',
                           '61a54a29c11331216aacd9a9a26786e1']
        cls.downloader = Downloader(cls.video, cls.test_hashes[0])

    def test_download_subs(self):
        self.downloader.download_subs()
        subs_file = self.downloader.video.path.with_suffix('.txt')
        self.assertTrue(subs_file.exists())
        with subs_file.open('rb') as file:
            contents = file.read()
        self.assertTrue(len(contents) > 100)
        subs_file.unlink()
