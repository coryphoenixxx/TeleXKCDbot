import re

from bs4 import BeautifulSoup
from shared.http_client import HttpClient
from yarl import URL

from scraper.dtos import XkcdTranslationData
from scraper.scrapers.base import BaseScraper


class XkcdDEScraper(BaseScraper):
    _BASE_URL = URL("https://xkcde.dapete.net/")

    def __init__(self, client: HttpClient):
        super().__init__(client=client)

    async def fetch_latest_number(self) -> int:
        soup = await self._get_soup(self._BASE_URL)

        xkcd_link = soup.find("p", {"class": "center"}).find("a").get("href")

        return int(
            re.match(
                pattern=re.compile(r".*.xkcd.com/(.*)/"),
                string=xkcd_link,
            ).group(1),
        )

    async def fetch_one(self, number: int, progress_bar=None) -> XkcdTranslationData | None:
        if number == 404:
            return

        url = self._BASE_URL.joinpath(str(number) + "/")
        soup = await self._get_soup(url, allow_redirects=False)

        if not len(soup):
            return

        data = XkcdTranslationData(
            number=number,
            source_link=url,
            title=self._extract_title(soup),
            tooltip=self._extract_tooltip(soup),
            image_url=await self._extract_image_url(soup),
            transcript_raw="",
            translator_comment=self._extract_comment(soup),
        )

        if progress_bar:
            progress_bar()

        return data

    def _extract_title(self, soup: BeautifulSoup) -> str:
        title_block = soup.find("h2", {"class": "comictitle"})
        title_block.span.decompose()

        return title_block.text.strip()

    def _extract_tooltip(self, soup: BeautifulSoup):
        return soup.find("figcaption").text

    async def _extract_image_url(self, soup: BeautifulSoup):
        large_version_block = soup.find("div", {"id": "large_version"})
        if large_version_block:
            large_image_page_url = large_version_block.find("a").get("href")
            soup = await self._get_soup(self._BASE_URL.joinpath(large_image_page_url[1:]))
            image_rel_path = soup.find("img").get("src")
        else:
            image_rel_path = soup.find("figure", {"id": "comic"}).find("img").get("src")

        return self._BASE_URL.joinpath(image_rel_path[1:])

    def _extract_comment(self, soup: BeautifulSoup):
        comment = ""
        comment_block = soup.find("div", {"id": "comments"})

        if comment_block:
            comment = comment_block.find("p").text

        return comment
