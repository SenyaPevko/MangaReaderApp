from PyQt6.QtCore import pyqtSignal, QThreadPool

from utils.database import Database
from Views.widgets.window_widgets.window_widget import WindowWidget


class MangaWindowWidget(WindowWidget):
    open_reader = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.threadpool = QThreadPool()
        self.scrapper = None
