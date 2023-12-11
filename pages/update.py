from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from pages.page import Page


class UpdatePage(Page):
    def __init__(self):
        super().__init__()

        text = "update"
        layout = QGridLayout()
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPixelSize(20)
        label.setFont(font)
        layout.addWidget(label)
        self.setLayout(layout)
