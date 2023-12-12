from PyQt6.QtCore import pyqtSignal, pyqtSlot, QThreadPool
from PyQt6.QtWidgets import QWidget

from utils.database import Database


class WindowWidget(QWidget):
    setup_done = pyqtSignal()
    setup_error = pyqtSignal()
    exit_page = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    @pyqtSlot()
    def close_widget(self):
        self.exit_page.emit()
