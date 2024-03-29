from PyQt6.QtCore import pyqtSignal, Qt, QThreadPool, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from models.manga import Manga
from models.manga_history import MangaHistory
from Views.ui.widgets.history_widget_ui import Ui_historyWidget
from utils.app_info import ICONS_PATH
from utils.database import Database
from utils.decorators import catch_exception
from utils.file_manager import FileManager
from utils.scrapper_manager import get_scrapper
from utils.threads import Worker
from utils.ui import set_icon


class HistoryWidget(QWidget):
    clicked_manga = pyqtSignal(Manga)
    clicked_chapter = pyqtSignal(list)
    delete_history = pyqtSignal(str)

    def __init__(self, manga_history: MangaHistory):
        super().__init__()
        self.ui = Ui_historyWidget()
        self.ui.setupUi(self)
        self.manga = None
        self.manga_pixmap = None
        self.threadpool = QThreadPool()
        self.page = manga_history.page
        self.chapter_name = manga_history.chapter_name
        self.chapter_number = manga_history.chapter_number
        self.scrapper = None
        self.db = Database()
        self.id = manga_history.id
        self.file_manager = FileManager()
        self.icon_path = rf"{ICONS_PATH}\delete.svg"
        self.icon_pixmap = None
        self.icon_max_size = QSize(25, 25)
        self.setup()

    def enterEvent(self, event):
        self.setProperty('is_set', 1)
        self.style().polish(self.ui.historyFrame)
        self.style().polish(self.ui.textFrame)
        self.style().polish(self.ui.mangaHistoryLabel)
        self.style().polish(self.ui.mangaNameLabel)
        self.style().polish(self.ui.image)
        self.style().polish(self.ui.deleteButton)

    def leaveEvent(self, event):
        self.setProperty('is_set', 0)
        self.style().polish(self.ui.historyFrame)
        self.style().polish(self.ui.textFrame)
        self.style().polish(self.ui.mangaNameLabel)
        self.style().polish(self.ui.mangaHistoryLabel)
        self.style().polish(self.ui.image)
        self.style().polish(self.ui.deleteButton)

    @catch_exception
    def setup(self):
        self.manga = self.db.get_manga_by_id(self.id)
        self.scrapper = get_scrapper(self.manga.scrapper)()
        self.setup_ui()

    @catch_exception
    def setup_ui(self):
        self.ui.mangaNameLabel.setText(self.manga.name)
        self.ui.mangaHistoryLabel.setText(f"Глава - {self.chapter_name} "
                                          f"Страница - {self.page}")
        self.ui.image.clicked.connect(lambda: self.clicked_manga.emit(self.manga))
        self.ui.mangaNameLabel.clicked.connect(self.open_reader)
        self.ui.mangaHistoryLabel.clicked.connect(self.open_reader)
        self.ui.deleteButton.clicked.connect(lambda: self.delete_history.emit(self.id))
        set_icon(self.icon_path, self.ui.deleteButton, self.icon_max_size)
        self.update_image()

    @catch_exception
    def get_image(self):
        path_to_save = self.file_manager.save_temp_preview(self.manga, {})
        self.manga_pixmap = QPixmap(path_to_save)

    @catch_exception
    def set_image(self):
        self.ui.image.clear()
        image_size = QSize(self.width(), self.height() - 20)
        pixmap = self.manga_pixmap.scaled(image_size, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
        self.ui.image.setPixmap(pixmap)

    @catch_exception
    def update_image(self):
        worker = Worker(self.get_image)
        worker.signals.finished.connect(self.set_image)
        self.threadpool.start(worker)

    @catch_exception
    def open_reader(self):
        self.clicked_chapter.emit([self.manga, self.scrapper.get_chapters(self.manga), self.chapter_number-1])

