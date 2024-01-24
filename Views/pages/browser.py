import os

from PyQt6.QtCore import QThreadPool, pyqtSignal
from PyQt6.QtGui import QIcon

from Views.windows.filters_dialog import FiltersDialog
from models.manga import Manga
from Views.pages.page import Page
from Views.ui.pages.browser_ui import Ui_Form
from utils import scrapper_manager
from utils.app_info import ICONS_PATH
from utils.decorators import catch_exception
from utils.threads import Worker

from Views.widgets.manga_scroll_area import MangaScrollArea
from scrappers.Manganelo import Manganelo
from Views.widgets.manga_preview_widget import MangaWidget


class BrowserPage(Page):
    manga_open = pyqtSignal(Manga)
    closed_icon_path = rf"{ICONS_PATH}\side_menu\browse_closed.svg"
    selected_icon_path = rf"{ICONS_PATH}\side_menu\browse_selected.svg"

    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.manga_scroll_area = MangaScrollArea(self.ui.mangasLayout)

        self.scrapper = None
        self.threadpool = QThreadPool()

        self.search_bar = self.ui.searchBar
        self.pages_list = self.ui.pagesList
        self.catalogs_list = self.ui.catalogList
        self.filters = None

        self.search_button = self.ui.searchButton
        self.filter_button = self.ui.filterButton
        self.page = 1
        self.request = ""
        self.added_genres = []
        self.removed_genres = []

        self.setup()

    @catch_exception
    def setup(self):
        self.set_catalog()
        self.set_filters()
        self.setup_ui()
        self.open_catalog(self.request, self.page)

    @catch_exception
    def set_catalog(self):
        self.set_catalogs_list()
        scrapper_name = self.catalogs_list.currentText()
        self.scrapper = scrapper_manager.get_scrapper(scrapper_name)()

    @catch_exception
    def set_filters(self):
        self.filters = FiltersDialog(self.scrapper.get_all_genres())
        self.filters.setWindowTitle("Фильтры")
        self.filters.setWindowIcon(QIcon(f"{ICONS_PATH}/Logo.png"))
        self.filters.accepted.connect(self.accept_filters)
        self.filters.discarded.connect(self.discard_filters)

    @catch_exception
    def setup_ui(self):
        self.catalogs_list.currentIndexChanged.connect(lambda: self.change_catalog())
        self.search_button.clicked.connect(lambda: self.open_catalog(self.search_bar.text(), 1))
        self.filter_button.clicked.connect(self.open_filters)
        self.search_bar.returnPressed.connect(lambda: self.open_catalog(self.search_bar.text(), 1))
        self.pages_list.currentIndexChanged.connect(
            lambda: self.get_content(self.request, self.pages_list.currentIndex() + 1))
        self.ui.nextPageButton.clicked.connect(
            lambda: self.get_content(self.request, self.pages_list.currentIndex() + 2))
        self.ui.previousPageButton.clicked.connect(
            lambda: self.get_content(self.request, self.pages_list.currentIndex()))

    @catch_exception
    def open_catalog(self, request, page):
        self.get_content(request, page)
        self.set_pages_list()

    def open_filters(self):
        self.filters.exec()

    @catch_exception
    def get_content(self, request: str, page: int):
        self.request = request
        if not (1 <= page <= len(self.pages_list)):
            return
        self.change_page(page)
        mangas = []
        worker = Worker(lambda: self.scrapper.get_content(request, page, self.added_genres, self.removed_genres))
        worker.signals.result.connect(lambda x: mangas.extend(x))
        worker.signals.finished.connect(lambda: self.add_content(mangas))
        self.threadpool.start(worker)

    @catch_exception
    def change_page(self, page):
        if page > self.pages_list.currentIndex() + 1:
            self.pages_list.setCurrentIndex(page - 1)
        elif page == self.pages_list.currentIndex():
            self.pages_list.setCurrentIndex(page - 1)
        self.page = page

    @catch_exception
    def add_content(self, mangas: list[Manga]):
        self.manga_scroll_area.delete_content()
        manga_list = []

        for manga in mangas:
            manga_widget = MangaWidget(manga)
            manga_widget.manga_clicked.connect(self.manga_open)
            manga_list.append(manga_widget)
        self.manga_scroll_area.add_content(manga_list)
        self.manga_scroll_area.update_content()

    @catch_exception
    def set_pages_list(self):
        self.pages_list.clear()
        for i in range(1, self.scrapper.get_catalog_pages() + 1):
            self.pages_list.addItem(str(i))

    @catch_exception
    def accept_filters(self):
        self.removed_genres = self.filters.get_removed_genres()
        self.added_genres = self.filters.get_selected_genres()
        self.open_catalog(self.search_bar.text(), 1)

    @catch_exception
    def discard_filters(self):
        if len(self.removed_genres) == 0 and len(self.added_genres) == 0:
            return
        
        self.removed_genres = []
        self.added_genres = []
        self.open_catalog(self.search_bar.text(), 1)

    @catch_exception
    def set_catalogs_list(self):
        self.catalogs_list.clear()
        scrappers_names = scrapper_manager.get_scrappers_names()
        for scrapper_name in scrappers_names:
            self.catalogs_list.addItem(scrapper_name)

    @catch_exception
    def change_catalog(self):
        self.setup()
