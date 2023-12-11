from models.chapter_page import ChapterPage
from models.chapter import Chapter
from scrappers.scrapper import Scrapper
from bs4 import BeautifulSoup
import requests
from models.manga import Manga


class Manganelo(Scrapper):
    USER_AGENT = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                                "like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
                  "Referer": "https://chapmanganelo.com/"}

    def __init__(self):
        super().__init__()
        self.name = "Manganelo"

    def search(self, request: str):
        source = requests.get("https://m.manganelo.com/search/story/" + "_".join(request.split())).text
        soup = BeautifulSoup(source, "lxml")

        for card in soup.find_all("div", class_="search-story-item"):
            name = card.find_next("a")["title"]
            url = card.find_next("a")["href"]
            image = card.find_next("img")["src"]
            scrapper = self.name
            id = self.get_manga_id(url)
            manga = Manga(name, url, image, scrapper, id)

            yield manga

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

    def get_chapters(self, manga: Manga):
        source = requests.get(manga.url).text
        soup = BeautifulSoup(source, "lxml")
        chapter_list = []
        for chapter in soup.find("ul", class_="row-content-chapter").findAll("li"):
            url = chapter.find("a")["href"]
            title = chapter.find("a")["title"]
            chapter_list.append(Chapter(url, title, "", "", manga.get_id(), manga.scrapper, url.split("-")[-1]))
        return chapter_list[::-1]

    def get_chapter_pages(self, chapter: Chapter):
        source = requests.get(chapter.url).text
        soup = BeautifulSoup(source, "lxml")
        count = 0
        pages_list = []
        for page in soup.find("div", class_="container-chapter-reader").find_all("img", class_="reader-content"):
            count += 1
            pages_list.append(ChapterPage(count, page["src"]))
        return pages_list

    def get_manga_id(self, manga_url):
        return manga_url.split("-")[-1]

    @staticmethod
    def get_user_agent():
        return Manganelo.USER_AGENT