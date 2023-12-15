from models.chapter import Chapter
from models.manga import Manga


class Scrapper:
    def __init__(self):
        self.name = None

    def search(self, request: str, page):
        pass

    def scrape_manga(self, manga: Manga):
        pass

    def get_chapters(self, manga: Manga):
        pass

    def get_chapter_pages(self, chapter: Chapter):
        pass

    def get_content(self, page, request):
        pass

    def get_all_genres(self):
        pass

    @staticmethod
    def get_user_agent():
        pass

