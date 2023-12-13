from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt

from utils import app_info
from utils.file_manager import FileManager
from widgets.window_widgets.window_widget import WindowWidget


class CacheWidget(WindowWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_manager = FileManager()

        text = f"В кэше хранятся изображения которые раньше открывались"
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPixelSize(20)
        label.setFont(font)

        delete_button = QPushButton("Очистить кэш")
        delete_button.setCursor(QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        delete_button.clicked.connect(self.file_manager.clear_temp)

        layout = QGridLayout()
        layout.addWidget(label)
        layout.addWidget(delete_button)
        self.setLayout(layout)

        self.setup_done.emit()