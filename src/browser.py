from typing import List, Dict, Union

import requests
from bs4 import BeautifulSoup
import re
import difflib

from src.common import parser_request
from src.exceptions import PyNapiTimeException

Movie = Dict[str, Union[str, int]]


def time_to_ms(timestr):
    extracted = re.search(r'(\d{2}):(\d{2}):(\d{2}).(\d*)', timestr).groups()
    time_ms = 0.0
    time_ms += float(extracted[0]) * 3600 * 1000
    time_ms += float(extracted[1]) * 60 * 1000
    time_ms += float(extracted[2]) * 1000
    time_ms += float(extracted[3])
    return time_ms


class Browser:
    FPS_ROUND_PRECISION = 2

    def __init__(self, video):
        self.video = video
        self.search_url = "http://napiprojekt.pl/ajax/search_catalog.php"
        self.root_url = "http://napiprojekt.pl/"
        self.use_scores = False
        self.movie = None
        self.subtitles_list = None

        self.video.collect_movie_data()

    def _get_movies(self) -> List[Movie]:
        """Returns search result of movies with similar titles from napi website."""

        TITLE_STR = "tytul"
        URL_STR = "href"

        values = {
            "associate": "",
            "queryKind": 0,
            "queryString": self.video.title,
            "queryYear": self.video.year,
        }
        movies_list = parser_request.post(self.search_url, values)
        movies = movies_list.findAll("a", class_="movieTitleCat")

        matched_movies = []
        for movie in movies:
            try:
                movie_info = dict(
                    title=movie[TITLE_STR],
                    href=movie[URL_STR],
                    year=int(
                        re.search(r"\d{4}", movie.h3.text).group(0)
                    ),
                )
            except AttributeError:
                "Year is not present on napiprojekt website, no movies matched."

            matched_movies.append(movie_info)

        return matched_movies

    @staticmethod
    def _similarity_score(title1, title2):
        return difflib.SequenceMatcher(None, title1, title2).ratio()

    def _get_movie(self) -> Movie:
        """Choose best matched movie from movies list."""
        movies = self._get_movies()
        if not self.video.year:
            # if no year is provided, detection cannot be performed, return first
            return movies[0]

        matched_by_year = self._filter_by_year(movies)
        movie = self._get_best_by_title_similarity(matched_by_year)
        print("Found match movie: %s" % movie["title"])
        return movie

    def _get_best_by_title_similarity(self, matched_by_year) -> Movie:
        matched_by_year_scores = [
            self._similarity_score(self.video.title, movie["title"]) for movie in matched_by_year
        ]
        max_score_idx = matched_by_year_scores.index(max(matched_by_year_scores))
        if self.use_scores:
            movie = matched_by_year[max_score_idx]
        else:
            movie = matched_by_year[0]
        return movie

    def _filter_by_year(self, movies):
        matched_by_year = [movie for movie in movies if movie["year"] == self.video.year]
        if not matched_by_year:
            if not self.video.title:
                raise ValueError("No matched movies found. Please add --title or change filename.")
            raise PyNapiTimeException(
                "No movies found for %s [%s]." % (self.video.title, self.video.year)
            )
        return matched_by_year

    @staticmethod
    def _get_soup_pages(soup_subtitles_page):
        """Iterate over pagination to get page urls."""
        pagination = soup_subtitles_page.findAll("span", class_="pagin")
        return [page.parent["href"] for page in pagination]

    def _extract_subtitles(self, page):
        subtitles_list = []
        if isinstance(page, BeautifulSoup):
            pass
        else:
            url = self.root_url + page
            res = requests.get(url)
            assert res.status_code == 200
            page = BeautifulSoup(res.content, "html.parser")

        subtitle_list_html = page.findAll("a", class_="tableA")
        for subtitle_html in subtitle_list_html:
            subtitles = subtitle_html.find_previous("tr")
            duration = subtitles.findAll("td")[3].p.string
            if duration:
                duration_ms = time_to_ms(duration)
            else:
                duration_ms = 0
            row = list(subtitle_html.parents)[2]
            metadata = row["title"]
            try:
                fps = re.search(r"FPS:</b> (\d{2}.\d{0,4})", metadata).group()
            except AttributeError:
                fps = None

            yield dict(
                    hash=subtitle_html["href"].split(":")[1],
                    duration=duration_ms,
                    fps_str=fps,
                    metadata=metadata,
                )

    def get_subtitles_list(self):
        self.movie = self._get_movie()
        movie_url = self._get_landing_page_url()
        first_subtitles_page_url = self._get_first_subtitles_page_url(movie_url)
        soup_first_subtitles_page = parser_request.get(first_subtitles_page_url)
        subtitles_pages = self._get_soup_pages(soup_first_subtitles_page)
        print("There are %s pages with subtitles." % len(subtitles_pages))

        subtitles_list = [subtitles for subtitles in self._subtitle_iterator(subtitles_pages)]
        self._check_subtitles_exists(subtitles_list)

        print("Found %s subtitles total." % len(subtitles_list))
        filtered_subtitles = self._clean_subtitles(subtitles_list)
        return filtered_subtitles

    def _check_subtitles_exists(self, subtitles_list):
        if not subtitles_list:
            raise PyNapiTimeException(
                "No subtitles found for movie %s[%s]."
                % (self.video.title, self.video.year)
            )

    def _subtitle_iterator(self, pages):
        for page in pages:
            for subtitle in self._extract_subtitles(page):
                yield subtitle

    def _get_first_subtitles_page_url(self, movie_url):
        # there is one intermediate page with movie metadata as landing page
        soup_landing_page = parser_request.post(movie_url)
        first_subtitle_page_path = soup_landing_page.find("a", string="napisy")["href"]
        return self.root_url + self._build_first_subtitles_url(first_subtitle_page_path)

    def _get_landing_page_url(self):
        return self.root_url + self.movie["href"]

    def _clean_subtitles(self, subtitles_list):
        video_fps = round(self.video.frame_rate, self.FPS_ROUND_PRECISION)
        for subtitles in subtitles_list:
            subtitles["duration_diff"] = abs(self.video.duration - subtitles["duration"])
            subtitles["fps"] = self._clean_fps(subtitles["fps_str"])
            subtitles["fps_diff"] = abs(subtitles["fps"] - video_fps)
        # sort to get best matches first, use fps diff to prioritize movies with same fps
        subtitles_list.sort(key=lambda x: (x["duration_diff"], x["fps_diff"]))
        return subtitles_list

    @classmethod
    def _clean_fps(cls, subtitles):
        if subtitles:
            fps_str = re.findall(r'(\d+\.\d+|\d+)', subtitles)[0]
            return round(float(fps_str), cls.FPS_ROUND_PRECISION)
        return 0

    def _build_first_subtitles_url(self, proxy_page_url):
        """Process first movie page, prepare for series."""
        if self.video.season or self.video.episode:
            if self.video.season and self.video.episode:
                proxy_page_url += f"-s{self.video.season}e{self.video.episode}"
            else:
                raise TypeError(
                    "Video is series but couldn't extract episode or season!")
        return proxy_page_url
