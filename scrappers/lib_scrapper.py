from models.manga import Manga
from utils.database import Database

# class LibScrapper:
#     def __init__(self):
#         self.db: Database = Database()
#         self.name = "Library"
#
#     def search_manga(self, params: RequestForm) -> list[Manga]:
#         manga = self.db.get_manga_library(params.lib_list)
#         return manga