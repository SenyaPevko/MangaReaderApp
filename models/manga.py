class Manga:
    def __init__(self, name, url, image, scrapper, id):
        self.name = name
        self.description = ""
        self.status = ""
        self.chapters = 0
        self.url = url
        self.image = image
        self.author = ""
        self.scrapper = scrapper
        self.genres = ""
        self.lib = ""
        self.id = id

    def get_id(self):
        return fr"{self.scrapper}_{self.id}"
