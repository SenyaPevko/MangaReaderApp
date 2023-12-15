from PyQt6.QtCore import Qt, QSize, QThreadPool, pyqtSlot
from PyQt6.QtGui import QPixmap

from models.chapter import Chapter
from models.manga import Manga
from models.manga_history import MangaHistory
from ui.widgets.reader_ui import Ui_Form
from utils.decorators import catch_exception
from utils.file_manager import FileManager
from utils.scrapper_manager import get_scrapper
from widgets.window_widgets.manga_window_widgets.manga_window_widget import MangaWindowWidget


class Reader(MangaWindowWidget):
    def __init__(self, manga: Manga, chapters: list[Chapter], current_chapter_index, parent):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.manga = manga
        self.chapters: list[Chapter] = chapters
        self.current_chapter_index = current_chapter_index
        self.current_page_number = 1
        self.pages = None
        self.images_area = self.ui.imagesScrollArea
        self.page_pixmap = None
        self.file_manager = FileManager()
        self.setup()

    @catch_exception
    def setup(self):
        self.setup_ui()
        self.scrapper = get_scrapper(self.manga.scrapper)()
        self.setup_chapters_list()
        self.setup_chapter()
        if not self.db.get_manga_by_id(self.manga.get_id()):
            self.db.add_manga(self.manga)

    @catch_exception
    def setup_ui(self):
        self.ui.nextPageButton.clicked.connect(self.turn_next_page)
        self.ui.previousPageButton.clicked.connect(self.turn_previous_page)
        self.ui.chaptersList.currentIndexChanged.connect(self.change_chapter)
        self.ui.exitButton.clicked.connect(self.close_widget)

    @pyqtSlot()
    def close_widget(self):
        self.save_chapter()
        self.save_manga_history()
        self.exit_page.emit()

    @pyqtSlot()
    def change_chapter(self):
        if self.current_chapter_index == self.ui.chaptersList.currentIndex():
            return
        self.save_chapter()
        self.save_manga_history()
        self.current_chapter_index = self.ui.chaptersList.currentIndex()
        self.setup_chapter()

    @catch_exception
    def save_chapter(self):
        if self.current_page_number != 1 and len(self.pages) != 1:
            self.db.add_chapter_history(self.chapters[self.current_chapter_index].get_id(), self.current_page_number,
                                        len(self.pages))

    @catch_exception
    def save_manga_history(self):
        self.db.add_manga_history(MangaHistory(self.manga.get_id(),
                                               self.chapters[self.current_chapter_index].title,
                                               self.current_chapter_index+1,
                                               self.current_page_number))

    @pyqtSlot()
    def turn_next_page(self):
        if self.current_page_number == len(self.pages):
            self.turn_next_chapter()
        else:
            self.current_page_number += 1
            self.setup_page()

    @pyqtSlot()
    def turn_previous_page(self):
        if self.current_page_number == 1:
            self.turn_previous_chapter()
        else:
            self.current_page_number -= 1
            self.setup_page()

    @catch_exception
    def turn_next_chapter(self):
        self.save_chapter()
        if self.current_chapter_index == len(self.chapters) - 1:
            self.exit_page.emit()
        else:
            self.current_chapter_index += 1
            self.setup_chapter()
            self.ui.chaptersList.setCurrentIndex(self.current_chapter_index)

    @catch_exception
    def turn_previous_chapter(self):
        if self.current_chapter_index == 0:
            return
        else:
            self.current_chapter_index -= 1
            self.setup_chapter()
            self.ui.chaptersList.setCurrentIndex(self.current_chapter_index)

    @catch_exception
    def setup_chapters_list(self):
        self.ui.chaptersList.clear()
        temp = self.current_chapter_index
        for chapter in self.chapters:
            self.ui.chaptersList.addItem(chapter.get_name())
        self.ui.chaptersList.setCurrentIndex(temp)
        self.current_chapter_index = temp

    @catch_exception
    def setup_chapter(self):
        self.current_page_number = 1
        pages_data = self.db.get_chapter_history(self.chapters[self.current_chapter_index].get_id())
        if pages_data is not None:
            self.current_page_number = pages_data[0]
        worker = Worker(self.get_content)
        worker.signals.error.connect(self.setup_error)
        worker.signals.finished.connect(self.setup_page)
        self.threadpool.start(worker)

    @catch_exception
    def setup_page(self):
        self.ui.pagesLabel.setText(f"Страница {self.current_page_number} из {len(self.pages)}")
        worker = Worker(self.get_image)
        worker.signals.error.connect(self.setup_error)
        worker.signals.finished.connect(self.set_image)
        self.setup_done.emit()
        self.threadpool.start(worker)

    @catch_exception
    def get_image(self):
        path_to_save = self.file_manager.save_temp_page(self.chapters[self.current_chapter_index],
                                                  self.pages[self.current_page_number - 1],
                                                  self.scrapper.get_user_agent())
        self.page_pixmap = QPixmap(path_to_save)

    @catch_exception
    def set_image(self):
        self.reset_images_area()
        self.resize_pixmap()
        self.ui.imageLabel.setPixmap(self.page_pixmap)

    @catch_exception
    def resize_image(self):
        self.resize_pixmap()
        self.ui.imageLabel.setPixmap(self.page_pixmap)

    @catch_exception
    def resize_pixmap(self):
        scroll_bar_policy = Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        width = self.images_area.viewport().width()
        height = self.page_pixmap.height()
        size = QSize(width, height)
        if 0.5 < self.page_pixmap.width() / self.page_pixmap.height() < 2:
            scroll_bar_policy = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            size = self.images_area.viewport().size()
        self.page_pixmap = self.page_pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio,
                                                   Qt.TransformationMode.SmoothTransformation)
        self.images_area.setVerticalScrollBarPolicy(scroll_bar_policy)

    @catch_exception
    def reset_images_area(self):
        self.ui.imageLabel.clear()
        self.images_area.verticalScrollBar().setValue(0)
        self.images_area.horizontalScrollBar().setValue(0)
        view_width = self.images_area.viewport().width()
        self.ui.imageLabel.setFixedWidth(view_width)
        self.ui.scrollAreaWidgetContents.setFixedWidth(view_width)
        self.ui.scrollAreaWidgetContents.resize(self.images_area.viewport().size())

    @catch_exception
    def get_content(self):
        self.pages = self.scrapper.get_chapter_pages(self.chapters[self.current_chapter_index])

    def resizeEvent(self, arg__1):
        super().resizeEvent(arg__1)
        if (self.page_pixmap is None) or (arg__1.oldSize() == arg__1.size()):
            return
        view_width = self.images_area.viewport().width()
        self.ui.imageLabel.setFixedWidth(view_width)
        self.ui.scrollAreaWidgetContents.setFixedWidth(view_width)
        self.ui.scrollAreaWidgetContents.resize(self.images_area.viewport().size())
        self.resize_image()
