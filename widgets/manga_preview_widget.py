from PyQt6.QtCore import Qt, QSize, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap

from models.manga import Manga
from ui.widgets.manga_preview_widget_ui import Ui_manga_widget
from utils.decorators import catch_exception
from utils.file_manager import FileManager
from utils.threads import Worker, ThreadPool


class MangaWidget(QWidget):
    manga_clicked = pyqtSignal(Manga)
    def __init__(self, manga):
        super().__init__()
        self.ui = Ui_manga_widget()
        self.ui.setupUi(self)
        self.manga = manga
        self.manga_pixmap = None
        self.ui.name.setText(self.manga.name)
        self.threadpool = QThreadPool()
        self.file_manager = FileManager()

    def enterEvent(self, event):
        self.setProperty('is_set', 1)
        self.style().polish(self.ui.manga_frame)
        self.style().polish(self.ui.name)
        self.style().polish(self.ui.image)

    def leaveEvent(self, event):
        self.setProperty('is_set', 0)
        self.style().polish(self.ui.manga_frame)
        self.style().polish(self.ui.name)
        self.style().polish(self.ui.image)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.rect().contains(event.pos()):
                self.manga_clicked.emit(self.manga)
        event.accept()

    @catch_exception
    def set_size(self, size: int):
        max_size = QSize(size, int(size * 1.6))
        if self.size() != max_size:
            self.setFixedSize(max_size)
            self.ui.image.setMaximumSize(max_size)
        if self.manga_pixmap:
            self.set_image()

    @catch_exception
    def get_image(self):
        path_to_save = self.file_manager.save_temp_preview(self.manga, {})
        self.manga_pixmap = QPixmap(path_to_save)

    @catch_exception
    def set_image(self):
        pixmap = self.manga_pixmap.scaled(self.ui.image.maximumSize(), Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
        self.ui.image.setPixmap(pixmap)

    @catch_exception
    def update_image(self):
        worker = Worker(self.get_image)
        worker.signals.finished.connect(self.set_image)
        self.threadpool.start(worker)
