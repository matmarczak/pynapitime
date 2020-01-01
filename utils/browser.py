import logging
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
import re
import difflib
from utils.exceptions import PyNapiTimeException, MovieNotFound

logger = logging.getLogger(__name__)

class Browser:
    def __init__(self, video):
        self.video = video
        self.search_url = "http://napiprojekt.pl/ajax/search_catalog.php"
        self.root_url = "http://napiprojekt.pl/"
        self.use_scores = False
        self.movie = None
        self.subtitles_list = None

    def get_matched_movies(self) -> List[Dict[str, str]]:
        TITLE_STR = "tytul"
        URL_STR = "href"

        values = {
            "associate": "",
            "queryKind": 0,
            "queryString": self.video.title,
            "queryYear": self.video.year,
        }

        res = requests.post(self.search_url, values)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")
        movies = soup.findAll("a", class_="movieTitleCat")

        matched_movies = []
        for movie in movies:
            try:
                movie_info = dict(
                    title=movie[TITLE_STR],
                    href=movie[URL_STR],
                    year=re.search(r"\d{4}", movie.h3.text).group(0),
                )
            except AttributeError:
                "Year is not present on napiprojekt website, no movies matched."

            matched_movies.append(movie_info)

        return matched_movies

    @staticmethod
    def similarity_score(title1, title2):
        return difflib.SequenceMatcher(None, title1, title2).ratio()

    @staticmethod
    def time_to_ms(x):
        time_ms = 0.0
        time_ms = time_ms + float(float(x.split(":")[0]) * 3600 * 1000)
        time_ms = time_ms + float(float(x.split(":")[1]) * 60 * 1000)
        time_ms = time_ms + float(float(x.split(":")[2]) * 1000)
        return time_ms

    def find_movie(self):
        movies = self.get_matched_movies()
        if not self.video.year:
            return movies[0]
        matched_by_year = [i for i in movies if int(i["year"]) == self.video.year]
        # naive string similarity comparison, needs support for title translation
        if not matched_by_year:
            if not self.video.title:
                raise ValueError("Please add movie title or change " "filename.")
            raise PyNapiTimeException(
                "No movies found for %s[%s]." % (self.video.title, self.video.year)
            )
        matched_by_year_scores = [
            self.similarity_score(self.video.title, i["title"]) for i in matched_by_year
        ]
        max_score_idx = matched_by_year_scores.index(max(matched_by_year_scores))
        if self.use_scores:
            movie = matched_by_year[max_score_idx]
        else:
            movie = matched_by_year[0]
        print("Found online movie: %s" % movie["title"])
        return movie

    @staticmethod
    def get_pages(content, current):
        pagination = content.findAll("span", class_="pagin")
        pages = [current["href"]]
        for i in pagination:
            if i.parent["href"] != current["href"]:
                pages.append(i.parent["href"])
        return pages

    def get_page_subs(self, page):
        logger.debug(f"Get subtitles from url {page}")
        subtitles_list = []
        if isinstance(page, BeautifulSoup):
            pass
        else:
            url = self.root_url + page
            res = requests.get(url)
            assert res.status_code == 200
            page = BeautifulSoup(res.content, "html.parser")

        subtitle_list_html = page.findAll("a", class_="tableA")
        for i in subtitle_list_html:
            subtitles = i.find_previous("tr")
            duration = subtitles.findAll("td")[3].p.string
            if duration:
                duration_ms = self.time_to_ms(duration)
            else:
                duration_ms = 0
            row = list(i.parents)[2]
            metadata = row["title"]
            try:
                fps = re.search(r"FPS:</b> (\d{2}.\d{0,4})", metadata).group()
            except AttributeError:
                fps = None

            subtitles_list.append(
                dict(
                    hash=i["href"].split(":")[1],
                    duration=duration_ms,
                    fps=fps,
                    metadata=metadata,
                )
            )

        return subtitles_list

    def get_subtitles_list(self):
        self.movie = self.find_movie()
        movie_url = self.root_url + self.movie["href"]
        logger.debug(f"Movie url is {movie_url}")

        res_movie = requests.post(movie_url)
        assert res_movie.status_code == 200
        soup_movie = BeautifulSoup(res_movie.content, "html.parser")
        # this is proxy page, scrape href and land to sbutitles page
        proxy_page_url_landing = soup_movie.find("a", string="napisy")
        if proxy_page_url_landing is None:
            raise MovieNotFound("Movie was not loaded properly from napiprojekt.")
        proxy_page_url = self.root_url + proxy_page_url_landing["href"]
        # get first subtitles page
        proxy_page_url = self._build_movie_page(proxy_page_url)
        logger.debug(f"Proxy page url is {proxy_page_url}")
        movie_page_res = requests.get(proxy_page_url)
        assert movie_page_res.status_code == 200
        movie_page = BeautifulSoup(movie_page_res.content, "html.parser")
        pages = self.get_pages(movie_page, proxy_page_url_landing)
        # page is already cached
        subs_page_1 = self.get_page_subs(movie_page)
        all_subs = subs_page_1
        print("There are %s pages with subtitles." % len(pages))

        for i in pages[1:]:
            all_subs += self.get_page_subs(movie_page)

        for i in all_subs:
            i["duration_diff"] = abs(self.video.duration - i["duration"])
        # sort to get best matches first
        all_subs.sort(key=lambda x: x["duration_diff"])
        if not all_subs:
            raise PyNapiTimeException(
                "No subtitles found for movie %s[%s]."
                % (self.video.title, self.video.year)
            )
        self.subtitles_list = all_subs
        print("Found %s versions of subtitles." % len(all_subs))
        return self.subtitles_list

    def _build_movie_page(self, proxy_page_url):
        if self.video.season or self.video.episode:
            if self.video.season and self.video.episode:
                proxy_page_url += f"-s{self.video.season}e{self.video.episode}"
            else:
                raise TypeError(
                    "Video is series but couldn't extract episode or season!")
        return proxy_page_url
