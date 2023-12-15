import os

from PyQt6.QtCore import pyqtSignal, pyqtSlot

from Enums.Libs import Libs
from models.manga import Manga
from pages.page import Page
from ui.pages.library_ui import Ui_Form
from utils.database import Database
from utils.decorators import catch_exception
from widgets.manga_preview_widget import MangaWidget
from widgets.manga_scroll_area import MangaScrollArea


class LibraryPage(Page):
    manga_open = pyqtSignal(Manga)
    closed_icon_path = rf"{os.getcwd()}\icons\side_menu\lib_closed.svg"
    selected_icon_path = rf"{os.getcwd()}\icons\side_menu\lib_selected.svg"

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.db = Database()
        self.lib_menu = self.ui.libsMenu
        self.manga_scroll_area = MangaScrollArea(self.ui.mangasLayout)
        self.search_bar = self.ui.searchBar

        self.setup()

    @catch_exception
    def setup(self):
        self.setup_ui()
        self.lib_menu.clear()
        self.set_libs_list()
        self.show_current_lib()

    @catch_exception
    def setup_ui(self):
        self.ui.searchButton.clicked.connect(lambda: self.search(self.search_bar.text()))
        self.search_bar.returnPressed.connect(lambda: self.search(self.search_bar.text()))
        self.lib_menu.currentIndexChanged.connect(self.show_current_lib)

    @catch_exception
    def set_libs_list(self):
        self.lib_menu.addItem(Libs.Reading.value)
        self.lib_menu.addItem(Libs.Planning.value)
        self.lib_menu.addItem(Libs.Dropped.value)

    @pyqtSlot()
    def show_current_lib(self):
        self.manga_scroll_area.delete_content()
        manga_list = []
        for manga in self.db.get_mangas_by_lib(self.lib_menu.currentText()):
            manga_widget = MangaWidget(manga)
            manga_widget.manga_clicked.connect(self.manga_open)
            manga_list.append(manga_widget)
        self.manga_scroll_area.add_content(manga_list)
        self.manga_scroll_area.update_content()

    @pyqtSlot()
    def search(self, request):
        self.manga_scroll_area.delete_content()
        manga_list = []
        for manga in self.db.get_mangas_by_lib(self.lib_menu.currentText()):
            if request.lower() not in manga.name.lower():
                continue
            manga_widget = MangaWidget(manga)
            manga_widget.manga_clicked.connect(self.manga_open)
            manga_list.append(manga_widget)
        self.manga_scroll_area.add_content(manga_list)
        self.manga_scroll_area.update_content()

    @catch_exception
    def update(self):
        self.show_current_lib()
