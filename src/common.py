import requests
from bs4 import BeautifulSoup


class ParserRequest:
    def __init__(self):
        self.session = requests.Session()

    def get(self, url, *args, **kwargs):
        return self._request("get", url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self._request("post", url, *args, **kwargs)

    def _request(self, method, url, *args, **kwargs):
        method = getattr(self.session, method)
        response = method(url, *args, **kwargs)
        response.raise_for_status()
        parsed_content = self._parse_content(response.content)
        return parsed_content

    def _parse_content(self, content):
        return BeautifulSoup(content, "html.parser")

parser_request = ParserRequest()
