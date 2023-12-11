import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget)
from PyQt6.QtGui import QIcon
from ui.windows.main_window_ui import Ui_MainWindow
from pages import browser, library, update, history, settings

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sidebar layout')
        self.setWindowIcon(QIcon("./icons/Logo.png"))

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.side_menu = self.ui.listWidget
        self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.main_content = self.ui.stackedWidget
        self.pages = ["library", "update", "history", "browser", "settings"]

        self.init_stackwidget()
        self.init_single_slot()

    def init_stackwidget(self):
            # Initialize the stack widget with content pages
            widget_list = self.main_content.findChildren(QWidget)
            for widget in widget_list:
                self.main_content.removeWidget(widget)

            lib_page = library.LibraryPage()
            self.main_content.addWidget(lib_page)

            update_page = update.UpdatePage()
            self.main_content.addWidget(update_page)

            history_page = history.HistoryPage()
            self.main_content.addWidget(history_page)

            browser_page = browser.BrowserPage()
            self.main_content.addWidget(browser_page)

            settings_page = settings.SettingsPage()
            self.main_content.addWidget(settings_page)

    def init_single_slot(self):

        # Connect signals and slots for switching between menu items
        self.side_menu.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)


def run():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())