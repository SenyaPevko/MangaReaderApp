from PyQt6 import QtCore
from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt, pyqtSlot

from utils.decorators import catch_exception
from utils.file_manager import FileManager
from Views.widgets.window_widgets.window_widget import WindowWidget


class CacheWidget(WindowWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_manager = FileManager()

        self.temp_size = self.file_manager.get_temp_size()
        self.text = (f"В кэше хранятся изображения которые раньше открывались\n"
                f"Занимаемая память: ")
        self.text_label = QLabel(f"{self.text}{self.temp_size}")
        self.delete_button = QPushButton("Очистить кэш")
        self.layout = QGridLayout()

        self.setup_ui()
        self.setup_done.emit()

    @catch_exception
    def setup_ui(self):
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPixelSize(20)
        self.text_label.setFont(font)

        self.delete_button.setCursor(QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.delete_button.clicked.connect(self.clear_temp)

        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)

    @catch_exception
    def update_text(self):
        self.temp_size = self.file_manager.get_temp_size()
        self.text_label.setText(f"{self.text}{self.temp_size}")

    @pyqtSlot()
    def clear_temp(self):
        self.file_manager.clear_temp()
        self.update_text()