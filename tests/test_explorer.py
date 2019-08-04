from unittest import TestCase
from unittest.mock import patch, Mock
from pathlib import Path
from tests.factories import MovieFilesFactory

import pytest

from utils.explorer import Explorer


class TestExplorer(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.movie_files = MovieFilesFactory()
        cls.explorer = Explorer(cls.movie_files.tempdir.name)

    def test_search_files(self):
        mock_iterdir = Mock()
        mock_iterdir.return_value = self.movie_files.movies.values()
        with patch("utils.explorer.Path.iterdir", mock_iterdir):
            self.explorer.search_files()
            self.assertEqual(len(self.explorer.no_subs_videos), 10)
            self.movie_files.movies[0].with_suffix(".txt").touch()
            self.explorer.search_files()
            self.assertEqual(len(self.explorer.no_subs_videos), 9)
