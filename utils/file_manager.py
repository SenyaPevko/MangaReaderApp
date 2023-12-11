import platformdirs
import re
import os
import shutil

import requests

from models.chapter_page import ChapterPage
from models.chapter import Chapter
from models.manga import Manga


class FileManager:
    TEMP_PATH = rf"{platformdirs.user_data_dir()}\MangaReaderAppTemp\Temp"
    TEMP_CHAPTERS = TEMP_PATH + r"\Chapters"
    TEMP_PREVIEWS = TEMP_PATH + r"\Previews"
    DOWNLOADS_PATH = rf"{platformdirs.user_data_dir()}\MangaReaderAppTemp\Downloads"

    @staticmethod
    def make_path(string):
        path_parts = []
        invalid_chars_pattern = r'[<>:"|?*\\/]'
        for path_part in string.split("/"):
            path_parts.append(re.sub(invalid_chars_pattern, "", path_part))
        return "".join(path_parts)

    @staticmethod
    def make_manga_preview_path(manga: Manga):
        path = rf"\{manga.scrapper}"
        file_name = rf"\{FileManager.make_path(manga.url)}.jpg"
        return path + file_name

    @staticmethod
    def make_chapter_page_path(chapter: Chapter, chapter_page: ChapterPage):
        path = rf"\{chapter.scrapper}\{FileManager.make_path(chapter.manga)}\{FileManager.make_path(chapter.url)}"
        file_name = rf"\{FileManager.make_path(str(chapter_page.page))}.jpg"
        return path + file_name

    @staticmethod
    def save_file(path, content):
        if FileManager.check_file_exists(path):
            return
        with open(path, "wb") as file:
            file.write(content)

    @staticmethod
    def save_temp_preview(manga: Manga, user_agent):
        path = FileManager.TEMP_PREVIEWS + FileManager.make_manga_preview_path(manga)
        FileManager.save_image(path, manga.image, user_agent)
        return path

    @staticmethod
    def save_temp_page(chapter: Chapter, chapter_page: ChapterPage, user_agent):
        path = FileManager.TEMP_CHAPTERS + FileManager.make_chapter_page_path(chapter, chapter_page)
        FileManager.save_image(path, chapter_page.img, user_agent)
        return path

    @staticmethod
    def save_image(path, image, user_agent):
        FileManager.create_directory(os.path.split(path)[0])
        image_content = requests.get(image, headers= user_agent).content
        FileManager.save_file(path, image_content)

    @staticmethod
    def get_temp_preview(manga: Manga):
        path = FileManager.TEMP_PREVIEWS + FileManager.make_manga_preview_path(manga)
        return path

    @staticmethod
    def get_temp_page(chapter: Chapter, chapter_page: ChapterPage):
        path = FileManager.TEMP_CHAPTERS + FileManager.make_chapter_page_path(chapter, chapter_page)
        return path

    @staticmethod
    def check_file_exists(path):
        return os.path.exists(path)

    @staticmethod
    def initialize_directories():
        FileManager.create_directory(FileManager.TEMP_PREVIEWS)
        FileManager.create_directory(FileManager.TEMP_CHAPTERS)
        FileManager.create_directory(FileManager.DOWNLOADS_PATH)

    @staticmethod
    def create_directory(path):
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)

    @staticmethod
    def clear_temp():
        for file in os.listdir(FileManager.TEMP_PATH):
            path = os.path.join(FileManager.TEMP_PATH, file)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(file)