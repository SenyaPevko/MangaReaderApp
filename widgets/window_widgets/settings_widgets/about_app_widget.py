from PyQt6.QtWidgets import  QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from utils import app_info
from widgets.window_widgets.window_widget import WindowWidget


class AboutAppWidget(WindowWidget):
    def __init__(self, parent):
        super().__init__(parent)

        text = f"made by Danil Kozlov \nVersion: {app_info.APP_VERSION}"
        layout = QGridLayout()
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPixelSize(20)
        label.setFont(font)
        layout.addWidget(label)
        self.setLayout(layout)

        self.setup_done.emit()