from utils.video import Video
from utils.browser import Browser
from utils.downloader import download_subs
from utils.explorer import Explorer
from utils.exceptions import PyNapiTimeException

from argparse import ArgumentParser
from pathlib import Path
import sys


def handle_file(path, args):
    video = Video(path, title=args.title, year=args.year)
    if video.subs_exist() and not args.force:
        print("Subtitles already exist. If you want to download anyway pass --force flag.")
    else:
        browser = Browser(video)
        try:
            subtitles = browser.get_subtitles_list()
        except PyNapiTimeException as e:
            print(str(e))
            return

        chosen_subs = subtitles[args.match - 1]
        print(
            "Choosed %s best match, which differs from video %s ms."
            % (args.match, chosen_subs["duration_diff"])
        )
        download_subs(video.path, chosen_subs["hash"])

        return


def main(args):
    parser = ArgumentParser(
        usage="download subtitles from napiprojekt based on movie duration"
    )
    parser.add_argument("path", type=str, help="path to video file")
    parser.add_argument(
        "-f",
        "--force",
        help="overwrite if subtitles exist",
        action="store_true",
    )
    parser.add_argument(
        "-m",
        "--match",
        help="specify index of subtitles sorted by duration difference, "
        "default 1 (lowest duration diff - ie 1st best match)",
        action="store",
        type=int,
        default=1,
    )
    parser.add_argument(
        "-t",
        "--title",
        help="specify title used to search for movie",
        action="store",
        type=str,
        default=None
    )
    parser.add_argument(
        "-y",
        "--year",
        help="specify year used to search for movie",
        action="store",
        type=int,
        default=None
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
