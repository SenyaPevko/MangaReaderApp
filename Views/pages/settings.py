from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal

from Views.pages.page import Page
from Views.ui.pages.settings_ui import Ui_Form
from utils.app_info import ICONS_PATH
from utils.decorators import catch_exception
from Views.widgets.settings_preview_widgets.cache_widget_preview import CachePreviewWidget
from Views.widgets.window_widgets.settings_widgets.about_app_widget import AboutAppWidget
from Views.widgets.settings_preview_widgets.about_app_widget_preview import AboutAppWidgetPreview
from Views.widgets.window_widgets.settings_widgets.cache_widget import CacheWidget
from Views.widgets.window_widgets.window_widget import WindowWidget


class SettingsPage(Page):
    widget_clicked = pyqtSignal(WindowWidget)
    closed_icon_path = rf"{ICONS_PATH}\side_menu\settings_closed.svg"
    selected_icon_path = rf"{ICONS_PATH}\side_menu\settings_selected.svg"

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

    @catch_exception
    def update(self):
        self.cache_preview_widget.update()
