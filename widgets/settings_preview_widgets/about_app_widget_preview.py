from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget

from ui.widgets.settings_widget_preview_ui import Ui_settingsWidget
from utils import app_info
from utils.decorators import catch_exception


class AboutAppWidgetPreview(QWidget):
    preview_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.ui = Ui_settingsWidget()
        self.ui.setupUi(self)

        self.setup()

    @catch_exception
    def setup(self):
        self.setup_ui()

    @catch_exception
    def setup_ui(self):
        self.ui.titleLabel.setText("О приложении")
        self.ui.descriptionLabel.setText(f"Версия: {app_info.APP_VERSION}")

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