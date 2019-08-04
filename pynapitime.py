from utils.video import Video
from utils.browser import Browser
from utils.downloader import download_subs
from utils.explorer import Explorer
from utils.exceptions import PyNapiTimeException

from argparse import ArgumentParser
from pathlib import Path
import sys


def handle_file(path, args):
    video = Video(path)
    video.collect_movie_data()
    if video.subs_exist() and not args.overwrite:
        print("Subtitles already exist. If you want to download anyway pass -o flag.")
    else:
        browser = Browser(video)
        try:
            subtitles = browser.get_subtitles_list()
        except PyNapiTimeException as e:
            print(str(e))
            return

        chosen_subs = subtitles[args.match]
        print(
            "Choosed %s best match, which differs from video %s ms."
            % (args.match + 1, chosen_subs["duration_diff"])
        )
        downloader = download_subs(video.path, chosen_subs["hash"])

        return


def main(args):
    parser = ArgumentParser(
        usage="download subtitles from napiprojekt based on movie duration"
    )
    parser.add_argument("path", type=str, help="path to video file")
    parser.add_argument(
        "-o",
        "--overwrite",
        help="if subtitles exist, script would overwrite",
        action="store_true",
    )
    parser.add_argument(
        "-m",
        "--match",
        help="specify index of subtitles sorted by duration diff, "
        "default 0 (best match)",
        action="store",
        type=int,
        default=0,
    )
    args = parser.parse_args(args)

    if Path(args.path).is_file():
        handle_file(args.path, args)
    else:
        explorer = Explorer(args.path)
        explorer.search_files()
        for i in explorer.no_subs_videos:
            handle_file(i.path, args)


if __name__ == "__main__":
    main(sys.argv[1:])
