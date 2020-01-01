import base64
import re

import requests
from pathlib import Path

url = "http://napiprojekt.pl/api/api-napiprojekt3.php"


def download_subs(path, movie_hash):
    path = Path(path)
    values = {
        "mode": "1",
        "client": "NapiProjektPython",
        "client_ver": "0.1",
        "downloaded_subtitles_id": movie_hash,
        "downloaded_subtitles_txt": "1",
        "downloaded_subtitles_lang": "PL",
    }
    res = requests.post(url, data=values)
    match = re.search(rb"DATA\[(?P<subs>.*)\]", res.content).group("subs")
    decoded = base64.b64decode(match)
    subs_file = path.with_suffix(".txt")
    subs_file.touch()
    with subs_file.open("wb") as file:
        file.write(decoded)
    print("Subtitles saved in {}".format(subs_file))
