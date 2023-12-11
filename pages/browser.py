from PyQt6.QtCore import QThreadPool, pyqtSignal

from models.manga import Manga
from pages.page import Page
from ui.pages.browser_ui import Ui_Form
from utils.threads import Worker

from widgets.manga_scroll_area import MangaScrollArea
from scrappers.Manganelo import Manganelo
from widgets.manga_preview_widget import MangaWidget


class BrowserPage(Page):
    manga_open = pyqtSignal(Manga)

    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.manga_scroll_area = MangaScrollArea(self.ui.mangasLayout)

        self.scrapper = Manganelo()
        self.threadpool = QThreadPool()

        self.search_bar = self.ui.searchBar
        self.pages_list = self.ui.pagesList

        self.search_button = self.ui.searchButton
        self.filter_button = self.ui.filterButton
        self.page = 1
        self.request = ""

        self.setup()

    def setup(self):
        self.setup_ui()
        self.open_catalog(self.request, self.page)

    def setup_ui(self):
        self.search_button.clicked.connect(lambda: self.open_catalog(self.search_bar.text(), 1))
        self.search_bar.returnPressed.connect(lambda: self.open_catalog(self.search_bar.text(), 1))
        self.pages_list.currentIndexChanged.connect(
            lambda: self.get_content(self.request, self.pages_list.currentIndex()+1))

    def open_catalog(self, request, page):
        self.get_content(request, page)
        self.set_pages_list()

    def get_content(self, request: str, page: int):
        self.request = request
        if not (1 <= page <= len(self.pages_list)):
            return
        self.page = page
        worker = Worker(lambda: self.scrapper.get_content(request, page))
        mangas = []
        worker.signals.result.connect(lambda x: mangas.extend(x))
        worker.signals.finished.connect(lambda: self.add_content(mangas))
        self.threadpool.start(worker)

    def add_content(self, mangas: list[Manga]):
        self.manga_scroll_area.delete_content()
        manga_list = []

        for manga in mangas:
            manga_widget = MangaWidget(manga)
            manga_widget.manga_clicked.connect(self.manga_open)
            manga_list.append(manga_widget)
        self.manga_scroll_area.add_content(manga_list)
        self.manga_scroll_area.update_content()

    def set_pages_list(self):
        self.pages_list.clear()
        for i in range(1, self.scrapper.get_catalog_pages()+1):
            self.pages_list.addItem(str(i))




