import re
from pathlib import Path
from .exceptions import BadFile
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
        """Checks is subtitles exist in directory."""
        extensions = [".txt", ".srt"]
        for i in extensions:
            # check for filename + ext and filename + its ext + subs ext
            if (
                self.path.with_suffix(i).exists()
                or self.path.with_suffix(self.path.suffix + i).exists()
            ):
                self.subtitles_exist = True
                return True
        return False

    @staticmethod
    def _extract_video_track(path):
        try:
            mediafile = MediaInfo.parse(path)
        except FileNotFoundError:
            raise
        except OSError:
            raise OSError("Mediainfo should be installed on system.")
        for i in mediafile.tracks:
            if i.track_type == "Video":
                video_track = i
                break
        return video_track

    def get_track_data(self):
        try:
            video_track = self._extract_video_track(self.path)
        except UnboundLocalError:
            raise BadFile("File doesn't contain video_track!")

        self.duration = video_track.duration
        self.frame_rate = video_track.frame_rate
        return None

    def extract(self, regex):
        pat = re.compile(regex)
        match = pat.search(self.path.name)
        if match:
            return match.group()
        return


    def extract_year(self):
        filename_movie_year = self.extract(r"(?P<year>(19|20|21)\d{2})")
        if filename_movie_year :
            return int(filename_movie_year)
        return

    def extrack_title(self):
        filename_movie_title = self.extract(r"(?P<title>.*)(p.)")
        human_readable_title = re.sub(r"\W", " ", filename_movie_title)
        title = human_readable_title.strip()
        return title

    def parse_name(self):
        self.title = self.extrack_title()
        self.year = self.extract_year()
        print("Title and year from filename are:")
        print("%s[%s]" % (self.title, self.year))

    def collect_movie_data(self):
        self.get_track_data()
        self.parse_name()
