import requests
import sys
import base64
import re


class Downloader:
    def __init__(self, video, movie_hash):
        self.video = video
        self.url = "http://napiprojekt.pl/api/api-napiprojekt3.php"
        self.movie_hash = movie_hash

    def download_subs(self, subs_hash=None):
        if not subs_hash:
            subs_hash = self.movie_hash

        values = {
            "mode": "1",
            "client": "NapiProjektPython",
            "client_ver": "0.1",
            "downloaded_subtitles_id": self.movie_hash,
            "downloaded_subtitles_txt": "1",
            "downloaded_subtitles_lang": "PL"
        }
        res = requests.post(self.url, data=values)
        match = re.search(rb'DATA\[(?P<subs>.*)\]', res.content).group('subs')
        decoded = base64.b64decode(match)
        subs_file = self.video._path.with_suffix('.txt')
        subs_file.touch()
        with subs_file.open('wb') as file:
            file.write(decoded)
