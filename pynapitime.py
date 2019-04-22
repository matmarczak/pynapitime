from pynapitime.video import Video
from pynapitime.browser import Browser
from pynapitime.downloader import Downloader
from pynapitime.explorer import Explorer
from pynapitime.exceptions import PyNapiTimeException

from argparse import ArgumentParser
from pathlib import Path


parser = ArgumentParser(
    usage="download subtitles from napiprojekt based on movie duration")
parser.add_argument('path', type=str, help="path to video file")
parser.add_argument('-o', '--overwrite',
                    help="if subtitles exist, script would overwrite",
                    action="store_true")
parser.add_argument('-m', '--match',
                    help="specify index of subtitles sorted by duration diff, "
                         "default 0 (best match)",
                    action="store", type=int, default=0)
args = parser.parse_args()

def handle_file(path):
    video = Video(path)
    video.collect_movie_data()
    if video.subs_exist() and not args.overwrite:
        print(
            "Subtitles already exist. If you want to download anyway pass -o flag.")
    else:
        browser = Browser(video)
        try:
            subtitles = browser.get_subtitles_list()
        except PyNapiTimeException as e:
            print(str(e))
            return None

        chosen_subs = subtitles[args.match]
        print('Choosed %s best match which differ from your video %s ms.' % (
            args.match + 1, chosen_subs['duration_diff']))
        downloader = Downloader(video, chosen_subs['hash'])
        downloader.download_subs()
        return None

if __name__ == "__main__":
        if Path(args.path).is_file():
            handle_file(args.path)
        else:
            explorer = Explorer(args.path)
            explorer.search_files()
            for i in explorer.no_subs_videos:
                handle_file(i.path)




