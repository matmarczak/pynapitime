from pynapitime.video import Video
from pynapitime.browser import Browser
from pynapitime.downloader import Downloader
from argparse import ArgumentParser

parser = ArgumentParser(usage="download subtitles from napiprojekt based on movie duration")
parser.add_argument('path', type=str, help="path to video file")
parser.add_argument('-o', '--overwrite', help="if subtitles exist script would overwrite", action="store_true")
parser.add_argument('-m', '--match', help="specify number of subtitles sorted by duration diff, default 0 (best match)",
                    action="store", type=int, default=0)
args = parser.parse_args()

if __name__ == "__main__":

    video = Video(args.path)
    video.collect_movie_data()
    if video.check_for_subs() and not args.overwrite:
        print("Subtitles already exist. If you want to download anyway pass -o flag.")
    else:
        browser = Browser(video)
        subtitles = browser.get_subtitles_list()
        chosen_subs = subtitles[args.match]
        print('Choosed %s best match which differ from your video %s ms.' % (
            args.match + 1, chosen_subs['duration_diff']))
        downloader = Downloader(video, chosen_subs['hash'])
        downloader.download_subs()
