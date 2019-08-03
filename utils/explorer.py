from pathlib import Path
from utils.video import Video


class Explorer:
    def __init__(self, path):
        self.path = Path(path)
        self.video_extentions = [".mkv", ".avi", ".mp4"]
        self.videos = None
        self.no_subs_videos = None

    def search_files(self):
        if not self.path.is_dir():
            return None
        self.videos = [
            Video(i) for i in self.path.iterdir() if i.suffix in self.video_extentions
        ]

        self.no_subs_videos = [i for i in self.videos if not i.subs_exist()]
        print("Found %s videos without subtitles!" % len(self.no_subs_videos))
        return None
