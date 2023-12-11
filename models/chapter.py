from models.manga import Manga


class Chapter:
    def __init__(self, url, title, volume, chapter, manga_id, scrapper_name, id):
        self.url = url
        self.title = title
        self.volume = volume
        self.chapter = chapter
        self.manga = manga_id
        self.scrapper = scrapper_name
        self.id = id

    def get_name(self):
        return self.title

    def get_id(self):
        return f"{self.manga}_{self.id}"