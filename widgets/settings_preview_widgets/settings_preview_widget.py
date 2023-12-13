import os

from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from ui.widgets.settings_widget_preview_ui import Ui_settingsWidget
from utils.decorators import catch_exception


class SettingsPreviewWidget(QWidget):
    preview_clicked = pyqtSignal()
    icons_path = rf"{os.getcwd()}\icons\settings_widgets"

    def __init__(self):
        super().__init__()

        self.ui = Ui_settingsWidget()
        self.ui.setupUi(self)
        self.icon_pixmap = None
        self.icon_max_size = QSize(30, 30)

    @catch_exception
    def set_icon(self, icon_path):
        self.ui.icon.setMaximumSize(self.icon_max_size)
        self.icon_pixmap = QPixmap(self.icons_path + icon_path)
        pixmap = self.icon_pixmap.scaled(self.ui.icon.maximumSize(), Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
        self.ui.icon.setPixmap(pixmap)

    def enterEvent(self, event):
        self.setProperty('is_set', 1)
        self.style().polish(self.ui.textFrame)
        self.style().polish(self.ui.widgetFrame)
        self.style().polish(self.ui.titleLabel)
        self.style().polish(self.ui.descriptionLabel)
        self.style().polish(self.ui.icon)

    def leaveEvent(self, event):
        self.setProperty('is_set', 0)
        self.style().polish(self.ui.textFrame)
        self.style().polish(self.ui.widgetFrame)
        self.style().polish(self.ui.titleLabel)
        self.style().polish(self.ui.descriptionLabel)
        self.style().polish(self.ui.icon)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.rect().contains(event.pos()):
                self.preview_clicked.emit()
        event.accept()