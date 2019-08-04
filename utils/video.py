import re
from pathlib import Path
from .exceptions import BadFile
from pymediainfo import MediaInfo
import PTN
import collections


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
        video_track = type("VideoTrack", (object,), {})
        video_track.duration = None
        video_track.frame_rate = None
        try:
            mediafile = MediaInfo.parse(path)
        except FileNotFoundError:
            raise
        except OSError:
            raise OSError("Mediainfo should be installed on system.")
        for i in mediafile.tracks:
            if i.duration and not video_track.duration:
                video_track.duration = i.duration
            if i.frame_rate and not video_track.frame_rate:
                video_track.frame_rate = i.frame_rate
        return video_track

    def get_track_data(self):
        try:
            video_track = self._extract_video_track(self.path)
        except TypeError:
            raise BadFile("Unable to extract movie duration.")

        self.duration = video_track.duration
        self.frame_rate = video_track.frame_rate
        return None

    def parse_name(self):
        info = PTN.parse(self.path.name)
        self.title = info.get("title")
        self.year = info.get("year", None)
        print("Title and year from filename are:")
        print("%s[%s]" % (self.title, self.year))

    def collect_movie_data(self):
        self.get_track_data()
        self.parse_name()
