from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal

from pages.page import Page
from ui.pages.settings_ui import Ui_Form
from utils.decorators import catch_exception
from widgets.settings_preview_widgets.cache_widget_preview import CachePreviewWidget
from widgets.window_widgets.settings_widgets.about_app_widget import AboutAppWidget
from widgets.settings_preview_widgets.about_app_widget_preview import AboutAppWidgetPreview
from widgets.window_widgets.settings_widgets.cache_widget import CacheWidget
from widgets.window_widgets.window_widget import WindowWidget


class SettingsPage(Page):
    widget_clicked = pyqtSignal(WindowWidget)

    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.about_app_preview_widget = AboutAppWidgetPreview()
        self.cache_preview_widget = CachePreviewWidget()

        self.setup()

    @catch_exception
    def setup(self):
        self.setup_ui()
        self.setup_widgets()

    @catch_exception
    def setup_widgets(self):
        self.ui.settingsWidgetsLayout.addWidget(self.about_app_preview_widget)
        self.about_app_preview_widget.ui.textFrame.setMaximumWidth(
            self.ui.settingsWidgetsLayout.maximumSize().width())
        self.about_app_preview_widget.preview_clicked.connect(
            lambda: self.widget_clicked.emit(AboutAppWidget(self)))

        self.ui.settingsWidgetsLayout.addWidget(self.cache_preview_widget)
        self.cache_preview_widget.ui.textFrame.setMaximumWidth(
            self.ui.settingsWidgetsLayout.maximumSize().width())
        self.cache_preview_widget.preview_clicked.connect(
            lambda: self.widget_clicked.emit(CacheWidget(self)))

    @catch_exception
    def setup_ui(self):
        self.ui.settingsWidgetsLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
