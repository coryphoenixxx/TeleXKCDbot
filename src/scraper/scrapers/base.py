from bs4 import BeautifulSoup
from shared.http_client import HttpClient
from yarl import URL


class BaseScraper:
    def __init__(
        self,
        client: HttpClient,
    ):
        self._client = client

    async def _get_soup(self, url: URL, **kwargs):
        async with self._client.safe_get(url=url, **kwargs) as response:
            html = await response.text()

        return BeautifulSoup(html, "lxml")
