from scrappers.Manganelo.ManganeloUrls import ManganeloUrls
from models.chapter_page import ChapterPage
from models.chapter import Chapter
from scrappers.scrapper import Scrapper
from bs4 import BeautifulSoup
import requests
from models.manga import Manga
import re

from utils.decorators import catch_exception


class Manganelo(Scrapper):
    USER_AGENT = {"Referer": "https://chapmanganelo.com/"}

    def __init__(self):
        super().__init__()
        self.name = "Manganelo"
        self.current_url = ManganeloUrls.Catalog.value

    @catch_exception
    def get_search_content(self, request: str, page: int):
        self.current_url = ManganeloUrls.Search.value
        source = requests.get(ManganeloUrls.Search.value
                              + "_".join(request.split())
                              + fr"?page={str(page)}").text
        soup = BeautifulSoup(source, "lxml")
        cards = soup.find_all("div", class_="search-story-item")

        return cards

    @catch_exception
    def get_catalog_content(self, page: int):
        self.current_url = ManganeloUrls.Catalog.value
        source = requests.get(f"{ManganeloUrls.Catalog.value}{page}").text
        soup = BeautifulSoup(source, "lxml")
        cards = soup.find_all("div", class_="content-genres-item")

        return cards

    @catch_exception
    def get_advanced_search_content(self, request, page, added_genres, removed_genres):
        added_genres_url_part = "" if len(added_genres) == 0 else "_" + "_".join(added_genres)
        removed_genres_url_part = "" if len(removed_genres) == 0 else "_" + "_".join(removed_genres)
        self.current_url = (f"{ManganeloUrls.AdvancedSearch.value}?s=all&g_i={added_genres_url_part}"
                            f"_&g_e={removed_genres_url_part}_&page={page}&keyw={request}")
        source = requests.get(self.current_url).text
        soup = BeautifulSoup(source, "lxml")
        cards = soup.find_all("div", class_="content-genres-item")

        return cards

    @catch_exception
    def get_content(self, request, page, added_genres: list[str], removed_genres: list[str]):
        if len(added_genres) > 0 or len(removed_genres) > 0:
            cards = self.get_advanced_search_content(request, page, added_genres, removed_genres)
        elif request == "":
            cards = self.get_catalog_content(page)
            self.current_url = ManganeloUrls.Catalog.value
        else:
            cards = self.get_search_content(request, page)
            self.current_url = (ManganeloUrls.Search.value
                                + "_".join(request.split())
                                + fr"?page={str(page)}")
        if cards is None:
            return []
        for card in cards:
            name = card.find_next("a")["title"]
            url = card.find_next("a")["href"]
            image = card.find_next("img")["src"]
            scrapper = self.name
            id = self.get_manga_id(url)
            manga = Manga(name, url, image, scrapper, id)

            yield manga

    @catch_exception
    def get_catalog_pages(self):
        try:
            source = requests.get(f"{self.current_url}").text
            soup = BeautifulSoup(source, "lxml")
            pages = soup.find("div", class_="group-page")
            page_text = pages.find_next("a", class_="page-blue page-last").text
            last_page = re.findall(r"[0-9]+", page_text)[0]
            return int(last_page)
        except Exception as e:
            print(e)

        return 1

    @catch_exception
    def scrape_manga(self, manga: Manga):
        source = requests.get(manga.url).text
        soup = BeautifulSoup(source, "lxml")
        manga.description = soup.find("div", class_="panel-story-info-description").text.strip()
        manga.chapters = len(soup.find("ul", class_="row-content-chapter").findAll("li"))
        tablet_rows = soup.find("table", class_="variations-tableInfo").findAll("tr")
        texts = {}
        for label in tablet_rows:
            key = label.find("td", class_="table-label").text.replace("\n", "").split()[0]
            value = label.find("td", class_="table-value").text.replace("\n", "")
            texts[key] = value
        manga.author = texts["Author(s)"]
        manga.status = texts["Status"]
        manga.genres = texts["Genres"]
        manga.id = manga.url.split("-")[-1]

        return manga

    @catch_exception
    def get_chapters(self, manga: Manga):
        source = requests.get(manga.url).text
        soup = BeautifulSoup(source, "lxml")
        chapter_list = []
        for chapter in soup.find("ul", class_="row-content-chapter").findAll("li"):
            url = chapter.find("a")["href"]
            title = chapter.find("a")["title"]
            chapter_list.append(Chapter(url, title, "", "", manga.get_id(),
                                        manga.scrapper, url.split("-")[-1]))

        return chapter_list[::-1]

    @catch_exception
    def get_chapter_pages(self, chapter: Chapter):
        source = requests.get(chapter.url).text
        soup = BeautifulSoup(source, "lxml")
        count = 0
        pages_list = []
        pages = (soup.find("div", class_="container-chapter-reader")
                 .find_all("img", class_="reader-content"))
        for page in pages:
            count += 1
            pages_list.append(ChapterPage(count, page["src"]))

        return pages_list

    @staticmethod
    def get_manga_id(manga_url):
        return manga_url.split("-")[-1]

    @catch_exception
    def get_all_genres(self):
        all_genres = {}
        source = requests.get(f"https://m.manganelo.com/genre-all-update-latest").text
        soup = BeautifulSoup(source, "lxml")
        genres = (soup.find("div", class_="advanced-search-tool-genres-list")
                  .find_all("span",
                            class_="advanced-search-tool-genres-item-choose advanced-search-tool-genres-item a-h text-nowrap"))
        for genre in genres:
            genre_id = genre["data-i"]
            genre_title = genre.text
            all_genres[genre_title] = genre_id

        return all_genres

    @staticmethod
    def get_user_agent():
        return Manganelo.USER_AGENT
