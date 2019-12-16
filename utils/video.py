from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip

from .exceptions import BadFile
import PTN


class Video:
    def __init__(self, path):
        self.path = Path(path)
        self.subtitles_exist = False
        self.duration = None
        self.year = None
        self.title = None
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
            clip = VideoFileClip(path.name)
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
            raise BadFile("Unable to extract movie duration.")
        return None

    def parse_name(self):
        info = PTN.parse(self.path.name)
        self.title = info.get("title")
        self.year = info.get("year")
        if info.get("season"):
            self.season = str(info.get("season")).zfill(2)
            self.episode = str(info.get("episode")).zfill(2)
        print("Title and year from filename are:")
        print("%s[%s]" % (self.title, self.year))

    def collect_movie_data(self):
        self.get_track_data()
        self.parse_name()
