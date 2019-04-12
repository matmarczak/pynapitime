from pathlib import Path
from pymediainfo import MediaInfo
import re
from collections import namedtuple

class Video:
    def __init__(self, path):
        self._path=Path(path)
        self.subtitles_exist = False
        self.duration = None
        self.year = None
        self.title = None
        self.frame_rate = None


    def check_for_subs(self):
        """Checks is subtitles exists in directory.
        """
        extensions = ['.txt','.srt']
        for i in extensions:
            # check for filename + ext and filename + its ext + subs ext
            x = self._path.with_suffix(self._path.suffix + i)
            if self._path.with_suffix(i).exists() or \
                    self._path.with_suffix(self._path.suffix + i).exists():
                self.subtitles_exist = True
                return True
        return False

    def get_track_data(self):
        mediafile = MediaInfo.parse(self._path)
        for i in mediafile.tracks:
            if i.track_type=='Video':
                video_track = i
                break
        self.duration = video_track.duration
        self.frame_rate = video_track.frame_rate
        return None

    def parse_name(self):
        #assume every filename has year which finishes title
        pat = re.compile(r'(?P<title>.*)(?=(?P<year>\d{4}))')
        match = pat.search(self._path.name)
        title = match.group('title')
        #replace separators with spaces
        human_readable_title = re.sub(r'\W', ' ', title)
        self.title = human_readable_title
        self.year = match.group('year')
        return None

    def gather_movie_data(self):
        if self.check_for_subs():
            print('Subtitles already exist.')
            return None
        else:
            self.get_track_data()
            self.parse_name()


