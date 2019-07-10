import re
from pathlib import Path

from pymediainfo import MediaInfo


class Video:
    def __init__(self, path):
        self.path = Path(path)
        self.subtitles_exist = False
        self.duration = None
        self.year = None
        self.title = None
        self.frame_rate = None

    def subs_exist(self):
        """Checks is subtitles exists in directory."""
        extensions = ['.txt', '.srt']
        for i in extensions:
            # check for filename + ext and filename + its ext + subs ext
            if self.path.with_suffix(i).exists() or \
                    self.path.with_suffix(self.path.suffix + i).exists():
                self.subtitles_exist = True
                return True
        return False

    def get_track_data(self):
        mediafile = MediaInfo.parse(self.path)
        for i in mediafile.tracks:
            if i.track_type == 'Video':
                video_track = i
                break
        self.duration = video_track.duration
        self.frame_rate = video_track.frame_rate
        return None

    def parse_name(self):
        # assume every filename has year which finishes title
        pat = re.compile(r'(?P<title>.*)(?=(?P<year>(19|20|21)\d{2}))')
        match = pat.search(self.path.name)
        title = match.group('title')
        # replace separators with spaces
        human_readable_title = re.sub(r'\W', ' ', title)
        self.title = human_readable_title
        self.year = match.group('year')
        print("Title and year from filename are:")
        print("%s[%s]" % (self.title, self.year))
        return None

    def collect_movie_data(self):
        self.get_track_data()
        self.parse_name()
