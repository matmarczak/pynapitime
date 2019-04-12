from pathlib import Path
from pymediainfo import MediaInfo


class Video:
    def __init__(self, path):
        self._path=Path(path)
        self.subtitles_exist = False

    def check_for_subs(self):
        """Checks is subtitles exists in directory.
        """
        extensions = ['.txt','.srt']
        for i in extensions:
            # check for filename + ext and filename + its ext + subs ext
            x = self._path.with_suffix(self._path.suffix + i)
            if self._path.with_suffix(i).exists() or \
                    self._path.with_suffix(self._path.suffix + i).exists():
                print('Subtitles already exist.')
                self.subtitles_exist = True
                return True
        return False

    def get_video_duration(self):
        czas = MediaInfo.parse(path)
        for track in czas.tracks:
            if track.track_type == 'Video':
                czas_trwania = track.duration

