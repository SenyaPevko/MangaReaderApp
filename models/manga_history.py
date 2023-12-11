class MangaHistory:
    def __init__(self, manga_id, chapter, page):
        self.id = manga_id
        self.chapter = chapter
        self.page = page

    def get_id(self):
        return self.id