from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip

from .exceptions import BadFile
import PTN


class Video:
    def __init__(self, path, title=None, year=None):
        self.path = Path(path)
        self.subtitles_exist = False
        self.duration = None
        self.year = year
        self.title = title
        self.frame_rate = None
        self.season = None
        self.episode = None

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
            clip = VideoFileClip(str(path))
        except FileNotFoundError:
            raise
        except OSError:
            raise
        duration_ms = clip.duration * 1000
        return duration_ms, clip.fps

    def get_track_data(self):
        try:
            self.duration, self.frame_rate = self._extract_video_track(self.path)
        except TypeError:
            raise BadFile("Unable to extract duration or fps.")
        return None

    def parse_name(self):
        info = PTN.parse(self.path.name)
        self._get_title_if_not_set(info)
        self._get_year_if_not_set(info)
        if info.get("season"):
            self.season = str(info.get("season")).zfill(2)
            self.episode = str(info.get("episode")).zfill(2)
        print("Title and year from filename are:")
        print("%s [%s]" % (self.title, self.year))

    def _get_year_if_not_set(self, info):
        if not self.year:
            self.year = info.get("year")

    def _get_title_if_not_set(self, info):
        if not self.title:
            self.title = info.get("title")

    def collect_movie_data(self):
        self.get_track_data()
        self.parse_name()
