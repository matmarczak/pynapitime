from unittest import TestCase
from pathlib import Path
from pynapitime.explorer import Explorer
from tests import config


class TestExplorer(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.explorer = Explorer(config.TEST_FOLDER_PATH)

    def test_search_for_files(self):
        file_path = Path('test_file.txt')
        file_path.touch()
        self.assertTrue(file_path.is_file())
        self.assertIsNone(Explorer(file_path).search_files())
        file_path.unlink()
        self.explorer.search_files()
        self.assertTrue(self.explorer.videos > 0)



