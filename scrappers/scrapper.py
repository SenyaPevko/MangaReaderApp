from models.chapter import Chapter
from models.manga import Manga


class Scrapper:
    def __init__(self):
        self.name = None

    def search(self, request: str):
        pass

    def scrape_manga(self, manga: Manga):
        pass

    def get_chapters(self, manga: Manga):
        pass

    def get_chapter_pages(self, chapter: Chapter):
        pass

    @staticmethod
    def get_user_agent():
        pass

