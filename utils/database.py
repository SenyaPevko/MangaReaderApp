import os
import sqlite3
from threading import Lock

import platformdirs
from models.manga import Manga
from models.manga_history import MangaHistory
from utils.decorators import with_lock_thread, singleton
from utils.file_manager import FileManager

@singleton
class Database(object):
    DIR_PATH = rf"{os.getcwd()}\MangaReaderAppTemp"
    FILE_NAME = r"\db.db"
    lock = Lock()

    def __init__(self):
        self.file_manager = FileManager()
        self.file_manager.create_directory(self.DIR_PATH)
        self.path = self.DIR_PATH + self.FILE_NAME
        self.file_manager.save_file(self.path, None)
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        self.setup_tabels()

    @with_lock_thread(lock)
    def add_manga(self, manga: Manga):
        self.cursor.execute("""INSERT INTO Mangas (id, name, description, status, chapters, url, image, author,
        scrapper, genres, library) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (manga.get_id(), manga.name, manga.description, manga.status,
                             manga.chapters, manga.url, manga.image, manga.author, manga.scrapper,
                             manga.genres, manga.lib))
        self.connection.commit()

    @with_lock_thread(lock)
    def get_manga_by_id(self, manga_id):
        manga_data = self.cursor.execute(f"SELECT * FROM Mangas WHERE id = ?", (manga_id,)).fetchone()
        self.connection.commit()
        if manga_data is None:
            return None
        name = manga_data[1]
        url = manga_data[5]
        image = manga_data[6]
        scrapper = manga_data[8]
        id = manga_data[0].split("_")[1]
        manga = Manga(name, url, image, scrapper, id)
        manga.description = manga_data[2]
        manga.status = manga_data[3]
        manga.chapters = manga_data[4]
        manga.author = manga_data[7]
        manga.genres = manga_data[9]
        manga.lib = manga_data[10]
        return manga

    @with_lock_thread(lock)
    def get_mangas_by_lib(self, lib):
        lib_data = self.cursor.execute(f"SELECT id FROM Mangas WHERE library = '{lib}'").fetchall()
        self.connection.commit()
        if not lib_data:
            return 
        for manga_data in lib_data:
            yield self.get_manga_by_id(manga_data[0])

    @with_lock_thread(lock)
    def update_manga_lib(self, manga_id, lib):
        self.cursor.execute("""Update Mangas set library = ? where id = ?""", (lib, manga_id))
        self.connection.commit()

    @with_lock_thread(lock)
    def remove_manga_by_id(self, manga_id):
        self.cursor.execute(f"DELETE FROM Mangas WHERE id = '{manga_id}'")
        self.connection.commit()

    @with_lock_thread(lock)
    def add_chapter_history(self, chapter_id, page_left_on, max_pages):
        self.cursor.execute("""INSERT INTO ChaptersHistory (id, page_left_on, max_pages) VALUES (?, ?, ?)""",
                            (chapter_id, page_left_on, max_pages))
        self.connection.commit()

    @with_lock_thread(lock)
    def get_chapter_history(self, chapter_id):
        chapter = self.cursor.execute(f"SELECT * FROM ChaptersHistory WHERE id = '{chapter_id}'").fetchone()
        self.connection.commit()
        if not chapter:
            return
        return chapter[1], chapter[2]

    @with_lock_thread(lock)
    def get_mangas_history(self):
        history_data = self.cursor.execute(f"SELECT * FROM MangasHistory").fetchall()
        self.connection.commit()
        if not history_data:
            return
        history_data.reverse()
        for data in history_data:
            yield MangaHistory(data[0], data[1], data[2], data[3])

    @with_lock_thread(lock)
    def add_manga_history(self, manga_history: MangaHistory):
        self.cursor.execute("""INSERT INTO MangasHistory (id, chapter_name, chapter_number, page) VALUES (?, ?, ?, ?)""",
                            (manga_history.get_id(),
                             manga_history.chapter_name,
                             manga_history.chapter_number,
                             manga_history.page))
        self.connection.commit()

    @with_lock_thread(lock)
    def remove_manga_history_id(self, manga_history_id):
        self.cursor.execute(f"DELETE FROM MangasHistory WHERE id = '{manga_history_id}'")
        self.connection.commit()

    @with_lock_thread(lock)
    def setup_tabels(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Mangas (id STRING PRIMARY KEY ON CONFLICT REPLACE NOT NULL,
        name STRING, description TEXT, status STRING, chapters INTEGER, url STRING, image STRING, 
        author STRING, scrapper STRING, genres STRING, library STRING);""")

        self.cursor.execute("CREATE INDEX IF NOT EXISTS library_name ON Mangas (library)")

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS ChaptersHistory (id STRING PRIMARY KEY ON CONFLICT REPLACE NOT NULL,
        page_left_on INTEGER, max_pages INTEGER);""")

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS MangasHistory (id STRING PRIMARY KEY ON CONFLICT REPLACE NOT NULL, 
            chapter_name STRING, chapter_number INTEGER, page INTEGER);""")
        self.connection.commit()