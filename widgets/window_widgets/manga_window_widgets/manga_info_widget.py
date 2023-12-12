from PyQt6.QtCore import QThreadPool, QSize, Qt, pyqtSlot
from PyQt6.QtGui import QPixmap, QBrush, QColor
from PyQt6.QtWidgets import QListWidgetItem

from Enums.BookMark import BookMark
from Enums.Libs import Libs
from models.manga import Manga
from utils.database import Database
from utils.decorators import catch_exception
from utils.scrapper_manager import get_scrapper
from ui.widgets.manga_info_widget_ui import Ui_Form
from utils.file_manager import FileManager
from utils.threads import Worker, ThreadPool
from widgets.window_widgets.manga_window_widgets.manga_window_widget import MangaWindowWidget
from widgets.window_widgets.window_widget import WindowWidget
from enum import Enum


class MangaInfoWidget(MangaWindowWidget):
    def __init__(self, manga: Manga, parent):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.manga = manga
        self.chapters = None
        self.chapters_list = self.ui.chaptersList
        self.setup()

    @catch_exception
    def setup(self):
        def scrape_manga():
            self.scrapper = get_scrapper(self.manga.scrapper)()
            self.manga = self.scrapper.scrape_manga(self.manga)

        self.setup_ui()
        worker = Worker(scrape_manga)
        worker.signals.error.connect(self.setup_error.emit)
        worker.signals.finished.connect(self.set_info)
        self.threadpool.start(worker)

    @catch_exception
    def setup_ui(self):
        self.ui.exitButton.clicked.connect(self.close_widget)
        self.ui.bookMarkButton.clicked.connect(
            lambda: self.add_manga_to_lib(self.ui.librariesList.currentText()))
        self.chapters_list.clicked.connect(self.open_reader)
        self.ui.librariesList.currentIndexChanged.connect(self.update_bookmark)

    @pyqtSlot()
    def set_info(self):
        self.ui.nameLabel.setText("Название: " + self.manga.name)
        self.ui.authorLabel.setText("Автор: " + self.manga.author)
        self.ui.statusLabel.setText("Статус: " + self.manga.status)
        self.ui.descriptionBrowser.setText(self.manga.description)
        self.ui.chaptersLabel.setText("Глав: " + str(self.manga.chapters))
        self.ui.genresLabel.setText("Жанры: " + self.manga.genres)
        self.file_manager = FileManager()
        self.set_preview_image()
        self.set_chapters()
        self.set_libs_list()
        self.set_bookmark()
        self.setup_done.emit()

    @catch_exception
    def set_bookmark(self):
        manga = self.db.get_manga_by_id(self.manga.get_id())
        if manga is not None:
            self.manga = manga
        else:
            self.add_manga_to_lib(Libs.No_Lib.value)

        if self.manga.lib is None or self.manga.lib == Libs.No_Lib.value:
            self.ui.bookMarkButton.setText(BookMark.Add.value)
            return
        else:
            for index in range(self.ui.librariesList.count()):
                if self.ui.librariesList.itemText(index) == self.manga.lib:
                    self.ui.librariesList.setCurrentIndex(index)
                    break
            self.ui.bookMarkButton.setText(BookMark.Added.value)
            return

    @pyqtSlot()
    def update_bookmark(self):
        if self.ui.librariesList.currentText() != self.manga.lib:
            self.ui.bookMarkButton.setText(BookMark.Add.value)
        else:
            self.ui.bookMarkButton.setText(BookMark.Added.value)

    @catch_exception
    def set_chapters(self):

        @catch_exception
        def get_chapters():
            self.chapters_list.clear()
            self.chapters_list.horizontalScrollBar()
            self.chapters = self.scrapper.get_chapters(self.manga)

        @catch_exception
        def setup_chapters():
            for chapter in self.chapters:
                pages_data = self.db.get_chapter_history(chapter.get_id())
                color = QColor(252, 251, 255)
                page = ""
                if pages_data is not None:
                    if pages_data[0] == pages_data[1]:
                        color = QColor(218, 242, 221)
                    else:
                        color = QColor(255, 238, 238)
                        page = f"Страница: {pages_data[0]}"
                item = QListWidgetItem(f"{chapter.get_name()} {page}")
                item.setBackground(QBrush(color))
                self.chapters_list.addItem(item)

        worker = Worker(get_chapters)
        worker.signals.error.connect(self.setup_error.emit)
        worker.signals.finished.connect(setup_chapters)
        self.threadpool.start(worker)

    @catch_exception
    def set_preview_image(self):
        self.ui.image.clear()
        image_size = QSize(self.width() // 3, self.height() // 2)
        image_path = self.file_manager.get_temp_preview(self.manga)
        manga_pixmap = QPixmap(image_path)
        pixmap = manga_pixmap.scaled(image_size, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
        self.ui.image.setPixmap(pixmap)

    @pyqtSlot()
    def add_manga_to_lib(self, lib: str):
        if lib == Libs.No_Lib.value and self.manga.lib == "":
            self.manga.lib = Libs.No_Lib.value
            self.db.add_manga(self.manga)
        elif self.manga.lib != lib:
            self.manga.lib = lib
            self.db.update_manga_lib(self.manga.get_id(), lib)
            self.update_bookmark()
        else:
            self.manga.lib = Libs.No_Lib.value
            self.db.update_manga_lib(self.manga.get_id(), self.manga.lib)
            self.update_bookmark()

    def set_libs_list(self):
        self.ui.librariesList.addItem(Libs.Reading.value)
        self.ui.librariesList.addItem(Libs.Planning.value)
        self.ui.librariesList.addItem(Libs.Dropped.value)

    def get_clicked_chapter_index(self):
        return self.chapters_list.indexFromItem(self.chapters_list.currentItem()).row()

    @catch_exception
    def update(self):
        self.set_chapters()

