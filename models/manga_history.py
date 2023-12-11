class MangaHistory:
    def __init__(self, manga_id, chapter_name, chapter_number, page):
        self.id = manga_id
        self.chapter_name = chapter_name
        self.chapter_number = chapter_number
        self.page = page

    def get_id(self):
        return self.id