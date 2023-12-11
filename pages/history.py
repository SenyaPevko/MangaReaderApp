from PyQt6.QtCore import Qt, pyqtSignal
from models.manga import Manga
from models.manga_history import MangaHistory
from pages.page import Page
from ui.pages.history_ui import Ui_Form
from utils.database import Database
from widgets.history_widget import HistoryWidget


class HistoryPage(Page):
    open_manga = pyqtSignal(Manga)
    open_reader = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.deleteButton.clicked.connect(self.delete_history)
        self.db = Database()
        self.history_widgets = []
        self.setup()

    def setup(self):
        self.setup_history_widgets()

    def delete_history(self):
        for history_widget in self.history_widgets:
            self.db.remove_manga_history_id(history_widget.id)
            self.ui.historyWidgetsLayout.removeWidget(history_widget)
            history_widget.deleteLater()
        self.history_widgets.clear()
        self.update()

    def setup_history_widgets(self):
        self.remove_history_widgets()
        self.add_history_widgets()

    def add_history_widgets(self):
        mangas_history = self.db.get_mangas_history()
        for manga_history in mangas_history:
            history_widget = HistoryWidget(manga_history)
            history_widget.clicked_manga.connect(self.open_manga)
            history_widget.clicked_chapter.connect(self.open_reader)
            history_widget.delete_history.connect(self.delete_manga_history)
            history_widget.ui.textFrame.setMaximumWidth(self.ui.historyWidgetsLayout.maximumSize().width())
            self.history_widgets.append(history_widget)
            self.ui.historyWidgetsLayout.addWidget(history_widget)

    def remove_history_widgets(self):
        for history_widget in self.history_widgets:
            self.ui.historyWidgetsLayout.removeWidget(history_widget)
            history_widget.deleteLater()
        self.history_widgets.clear()

    def update(self):
        self.setup()

    def delete_manga_history(self, id: str):
        for history_widget in self.history_widgets:
            if history_widget.id == id:
                break
        self.db.remove_manga_history_id(history_widget.id)
        self.history_widgets.remove(history_widget)
        self.ui.historyWidgetsLayout.removeWidget(history_widget)
        history_widget.deleteLater()
        self.update()