from PyQt6.QtCore import QThreadPool, pyqtSignal

from models.manga import Manga
from pages.page import Page
from ui.pages.browser_ui import Ui_Form

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
        self.search_bar.returnPressed.connect(lambda: self.search(self.search_bar.text()))

        self.search_button = self.ui.searchButton
        self.search_button.clicked.connect(lambda: self.search(self.search_bar.text()))

        self.filter_button = self.ui.filterButton

    def search(self, request):
        self.manga_scroll_area.delete_content()
        manga_list = []

        for manga in self.scrapper.search(request):
            manga_widget = MangaWidget(manga)
            manga_widget.manga_clicked.connect(self.manga_open)
            manga_list.append(manga_widget)
        self.manga_scroll_area.add_content(manga_list)
        self.manga_scroll_area.update_content()





