import tempfile
import unittest
import pathlib
from pynapitime.downloader import download_subs


class TestDownloader(unittest.TestCase):
    test_hashes = ['34e51a07ab99cec163136ae1998363a6',
                   '74dc8c6afe25f34dcb24e591316e64d3',
                   '61a54a29c11331216aacd9a9a26786e1']

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.path = cls.tempdir
        cls.temp_movie = pathlib.Path(cls.path.name) / "Jumanji.Welcome.to.the.Jungle.2017.480p.BluRay.x264.mkv"
        cls.temp_movie.touch()

    def test_download_subs(self):
        for i in self.test_hashes:
            download_subs(self.temp_movie.resolve(), i)
            subs_file = self.temp_movie.with_suffix('.txt')
            self.assertTrue(subs_file.exists())
            with subs_file.open('rb') as file:
                contents = file.read()
            self.assertTrue(len(contents) > 100)
            subs_file.unlink()
