import platformdirs
import re
import os
import shutil
from pathlib import Path

import requests

from models.chapter_page import ChapterPage
from models.chapter import Chapter
from models.manga import Manga
from utils.decorators import singleton


@singleton
class FileManager:
    TEMP_PATH = rf"{os.getcwd()}\MangaReaderAppTemp\Temp"
    TEMP_CHAPTERS = TEMP_PATH + r"\Chapters"
    TEMP_PREVIEWS = TEMP_PATH + r"\Previews"
    DOWNLOADS_PATH = rf"{os.getcwd()}\MangaReaderAppTemp\Downloads"

    def __init__(self):
        self.initialize_directories()

    def make_path(self, string):
        path_parts = []
        invalid_chars_pattern = r'[<>:"|?*\\/]'
        for path_part in string.split("/"):
            path_parts.append(re.sub(invalid_chars_pattern, "", path_part))
        return "".join(path_parts)

    def make_manga_preview_path(self, manga: Manga):
        path = rf"\{manga.scrapper}"
        file_name = rf"\{self.make_path(manga.url)}.jpg"
        return path + file_name

    def make_chapter_page_path(self, chapter: Chapter, chapter_page: ChapterPage):
        path = rf"\{chapter.scrapper}\{self.make_path(chapter.manga)}\{self.make_path(chapter.url)}"
        file_name = rf"\{self.make_path(str(chapter_page.page))}.jpg"
        return path + file_name

    def save_file(self, path, content):
        if self.check_file_exists(path):
            return
        with open(path, "wb") as file:
            file.write(content)

    def save_temp_preview(self, manga: Manga, user_agent):
        path = self.TEMP_PREVIEWS + self.make_manga_preview_path(manga)
        self.save_image(path, manga.image, user_agent)
        return path

    def save_temp_page(self, chapter: Chapter, chapter_page: ChapterPage, user_agent):
        path = self.TEMP_CHAPTERS + self.make_chapter_page_path(chapter, chapter_page)
        self.save_image(path, chapter_page.img, user_agent)
        return path

    def save_image(self, path, image, user_agent):
        self.create_directory(os.path.split(path)[0])
        image_content = requests.get(image, headers=user_agent).content
        self.save_file(path, image_content)

    def get_temp_preview(self, manga: Manga):
        path = self.TEMP_PREVIEWS + self.make_manga_preview_path(manga)
        return path

    def get_temp_page(self, chapter: Chapter, chapter_page: ChapterPage):
        path = self.TEMP_CHAPTERS + self.make_chapter_page_path(chapter, chapter_page)
        return path

    def check_file_exists(self, path):
        return os.path.exists(path)

    def initialize_directories(self):
        self.create_directory(self.TEMP_PREVIEWS)
        self.create_directory(self.TEMP_CHAPTERS)
        self.create_directory(self.DOWNLOADS_PATH)

    def create_directory(self, path):
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)

    def clear_directory(self, path_to_clear):
        for file in os.listdir(path_to_clear):
            path = os.path.join(path_to_clear, file)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(file)

    def clear_temp(self):
        self.clear_directory(self.TEMP_CHAPTERS)
        self.clear_directory(self.TEMP_PREVIEWS)

    def get_temp_size(self):
        temp_size = self.get_directory_size(self.TEMP_PATH)
        return self.parse_file_size(temp_size)

    def get_directory_size(self, path):
        return sum(p.stat().st_size for p in Path(path).rglob('*'))

    def parse_file_size(self, size):
        for unit in ("B", "K", "M", "G", "T"):
            if size < 1024:
                break
            size /= 1024
        return f"{size:.1f}{unit}"