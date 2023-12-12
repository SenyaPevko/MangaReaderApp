from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal

from pages.page import Page
from ui.pages.settings_ui import Ui_Form
from utils.decorators import catch_exception
from widgets.window_widgets.settings_widgets.about_app_widget import AboutAppWidget
from widgets.settings_preview_widgets.about_app_widget_preview import AboutAppWidgetPreview
from widgets.window_widgets.window_widget import WindowWidget


class SettingsPage(Page):
    widget_clicked = pyqtSignal(WindowWidget)

    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.about_app_widget_preview = AboutAppWidgetPreview()

        self.setup()

    @catch_exception
    def setup(self):
        self.setup_ui()
        self.setup_widgets()

    def setup_widgets(self):
        self.ui.settingsWidgetsLayout.addWidget(self.about_app_widget_preview)
        self.about_app_widget_preview.ui.textFrame.setMaximumWidth(
            self.ui.settingsWidgetsLayout.maximumSize().width())

        self.about_app_widget_preview.preview_clicked.connect(
            lambda: self.widget_clicked.emit(AboutAppWidget(self)))

    @catch_exception
    def setup_ui(self):
        self.ui.settingsWidgetsLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
