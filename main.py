import sys
from PyQt6.QtCore import Qt, QFile, QTextStream, QSize, pyqtSlot
from PyQt6.QtWidgets import (QApplication, QMainWindow)
from PyQt6.QtGui import QIcon

from models.chapter import Chapter
from models.manga import Manga
from pages.page import Page
from ui.windows.main_window_ui import Ui_MainWindow
from pages import browser, library, update, history, settings
from widgets.window_widgets.manga_window_widgets.manga_info_widget import MangaInfoWidget
from widgets.window_widgets.manga_window_widgets.reader import Reader
from widgets.window_widgets.window_widget import WindowWidget


# pyuic6.exe .\settings_widget_preview.ui -o .\settings_widget_preview_ui.py

class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.set_style()

    def get_style(self):
        widgets = self.read_file(QFile("ui/styles/widgets.qss"))
        style = widgets
        return style

    def read_file(self, file: QFile):
        file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        stream = QTextStream(file)
        return stream.readAll()

    def set_style(self):
        self.setStyleSheet(self.get_style())


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sidebar layout')
        self.setWindowIcon(QIcon("./icons/Logo.png"))
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
        self.page = self.pages_widget.currentWidget()

        self.setup_connections()

    def setup_connections(self):
        self.browser_page.manga_open.connect(lambda manga: self.open_info(manga, self.browser_page))
        self.library_page.manga_open.connect(lambda manga: self.open_info(manga, self.library_page))
        self.history_page.open_manga.connect(lambda manga: self.open_info(manga, self.history_page))
        self.history_page.open_reader.connect(
            lambda args: self.open_reader(args[0], args[1], args[2], self.history_page))

        self.ui.browserButton.clicked.connect(lambda: self.change_page(self.browser_page))
        self.ui.historyButton.clicked.connect(lambda: self.change_page(self.history_page))
        self.ui.updateButton.clicked.connect(lambda: self.change_page(self.update_page))
        self.ui.libraryButton.clicked.connect(lambda: self.change_page(self.library_page))
        self.ui.settingsButton.clicked.connect(lambda: self.change_page(self.settings_page))

        self.settings_page.widget_clicked.connect(self.set_widget)

    @pyqtSlot(Page)
    def change_page(self, page: Page):
        current_widget = self.pages_widget.currentWidget()
        if current_widget != page:
            if isinstance(current_widget, WindowWidget):
                self.delete_widget(current_widget)
                current_widget.close_widget()
            self.pages_widget.removeWidget(self.pages_widget.currentWidget())
            page.update()
            self.pages_widget.addWidget(page)
            self.pages_widget.setCurrentWidget(page)
            self.page = page

    @pyqtSlot(WindowWidget)
    def open_widget(self, widget: WindowWidget):
        self.pages_widget.setEnabled(False)
        widget.setup_done.connect(lambda: self.set_widget(widget))
        widget.setup_error.connect(lambda: self.delete_widget(widget))
        widget.exit_page.connect(lambda: self.delete_widget(widget))

    @pyqtSlot(WindowWidget)
    def set_widget(self, widget: WindowWidget):
        self.pages_widget.addWidget(widget)
        self.pages_widget.setCurrentWidget(widget)
        self.pages_widget.setEnabled(True)

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


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor)
    app = App(sys.argv)
    with open("ui/styles/widgets.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
