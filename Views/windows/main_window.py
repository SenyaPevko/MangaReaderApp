import os

from PyQt6.QtCore import QSize, pyqtSlot, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel

from models.chapter import Chapter
from models.manga import Manga
from Views.pages import library, update, history, browser, settings
from Views.pages.page import Page
from Views.ui.windows.main_window_ui import Ui_MainWindow
from utils.app_info import ICONS_PATH
from utils.decorators import catch_exception
from Views.widgets.window_widgets.manga_window_widgets.manga_info_widget import MangaInfoWidget
from Views.widgets.window_widgets.manga_window_widgets.reader import Reader
from Views.widgets.window_widgets.window_widget import WindowWidget
from utils.ui import set_icon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(f"{ICONS_PATH}/Logo.png"))
        self.ui = Ui_MainWindow()
        self.setMinimumSize(QSize(
            self.screen().size().width() // 2,
            self.screen().size().height() // 2))
        self.ui.setupUi(self)

        self.library_page = library.LibraryPage()
        self.update_page = update.UpdatePage()
        self.history_page = history.HistoryPage()
        self.browser_page = browser.BrowserPage()
        self.settings_page = settings.SettingsPage()

        self.pages_widget = self.ui.stackedWidget
        self.pages_widget.addWidget(self.library_page)
        self.current_page = self.pages_widget.currentWidget()
        self.current_page_button = self.ui.libraryButton

        self.closed_icon_max_size = QSize(28, 28)
        self.opened_icon_max_size = QSize(60, 60)

        self.setup_connections()
        self.setup_side_menu_icons()

    def setup_connections(self):
        self.browser_page.manga_open.connect(lambda manga: self.open_info(manga, self.browser_page))
        self.library_page.manga_open.connect(lambda manga: self.open_info(manga, self.library_page))
        self.history_page.open_manga.connect(lambda manga: self.open_info(manga, self.history_page))
        self.history_page.open_reader.connect(
            lambda args: self.open_reader(args[0], args[1], args[2], self.history_page))

        self.ui.browserButton.clicked.connect(
            lambda: self.change_page(self.browser_page, self.ui.browserButton))
        self.ui.historyButton.clicked.connect(
            lambda: self.change_page(self.history_page, self.ui.historyButton))
        self.ui.updateButton.clicked.connect(
            lambda: self.change_page(self.update_page, self.ui.updateButton))
        self.ui.libraryButton.clicked.connect(
            lambda: self.change_page(self.library_page, self.ui.libraryButton))
        self.ui.settingsButton.clicked.connect(
            lambda: self.change_page(self.settings_page, self.ui.settingsButton))
        self.settings_page.widget_clicked.connect(self.set_widget)

    @catch_exception
    def setup_side_menu_icons(self):
        set_icon(self.browser_page.closed_icon_path,
                 self.ui.browserButton, self.closed_icon_max_size)
        set_icon(self.update_page.closed_icon_path,
                 self.ui.updateButton, self.closed_icon_max_size)
        set_icon(self.history_page.closed_icon_path,
                 self.ui.historyButton, self.closed_icon_max_size)
        set_icon(self.library_page.selected_icon_path,
                 self.ui.libraryButton, self.opened_icon_max_size)
        set_icon(self.settings_page.closed_icon_path,
                 self.ui.settingsButton, self.closed_icon_max_size)

        self.ui.browserButton.setAlignment(Qt.AlignmentFlag.AlignCenter)

    @pyqtSlot(Page, QLabel)
    def change_page(self, page: Page, page_button: QLabel):
        current_widget = self.pages_widget.currentWidget()
        if current_widget != page:
            if isinstance(current_widget, WindowWidget):
                current_widget.close_widget()
            if self.current_page != page:
                self.pages_widget.removeWidget(self.pages_widget.currentWidget())
                page.update()
                set_icon(page.selected_icon_path, page_button, self.opened_icon_max_size)
                set_icon(self.current_page.closed_icon_path, self.current_page_button,
                         self.closed_icon_max_size)
                self.pages_widget.addWidget(page)
                self.pages_widget.setCurrentWidget(page)
                self.current_page = page
                self.current_page_button = page_button

    @pyqtSlot(WindowWidget)
    def open_widget(self, widget: WindowWidget):
        self.pages_widget.setEnabled(False)
        widget.setup_done.connect(lambda: self.set_widget(widget))
        widget.setup_error.connect(lambda: self.delete_widget(widget))

    @pyqtSlot(WindowWidget)
    def set_widget(self, widget: WindowWidget):
        self.pages_widget.addWidget(widget)
        self.pages_widget.setCurrentWidget(widget)
        self.pages_widget.setEnabled(True)
        widget.exit_page.connect(lambda: self.delete_widget(widget))

    @pyqtSlot(WindowWidget)
    def delete_widget(self, widget: WindowWidget):
        widget.deleteLater()
        widget.parent.update()
        self.pages_widget.setEnabled(True)

    @pyqtSlot(Manga)
    def open_info(self, manga: Manga, parent):
        info = MangaInfoWidget(manga, parent)
        self.open_widget(info)
        info.open_reader.connect(lambda: self.open_reader(info.manga, info.chapters, info.get_clicked_chapter_index(),
                                                          info))
    @pyqtSlot()
    def open_reader(self, manga: Manga, chapters: list[Chapter], chapter_index, parent):
        reader = Reader(manga, chapters, chapter_index, parent)
        self.open_widget(reader)