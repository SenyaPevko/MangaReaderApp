from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QLabel

from utils.decorators import catch_exception
from Views.widgets.manga_preview_widget import MangaWidget


class MangaScrollArea(QScrollArea):
    def __init__(self, parent):
        super().__init__()
        self.setWidgetResizable(True)
        self.column_count = 7
        self.manga_list = []

        self.scroll_area_content = QWidget()
        self.scroll_area_content.setObjectName("scroll_area_content")
        self.scroll_area_content.resizeEvent = self.scroll_resize_event

        self.scroll_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)

        self.content_grid = QGridLayout()
        self.content_grid.setVerticalSpacing(12)

        self.scroll_layout.addLayout(self.content_grid)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.scroll_layout.addItem(self.vertical_spacer)
        self.setWidget(self.scroll_area_content)

        self.is_empty_label = None

        if parent is not None:
            parent.addWidget(self)

    @catch_exception
    def scroll_resize_event(self, event):
        if event.oldSize().width() != event.size().width():
            self.update_content()
        event.accept()

    @catch_exception
    def add_content(self, manga_list: list[MangaWidget]):
        raw_count, column_count = 0, 0
        for manga in manga_list:
            self.manga_list.append(manga)
            self.content_grid.addWidget(manga, raw_count, column_count,
                                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            manga.update_image()
            column_count += 1
            if column_count == self.column_count - 1:
                column_count = 0
                raw_count += 1
        self.is_content_empy()

    @catch_exception
    def delete_content(self):
        self.verticalScrollBar().setValue(0)
        for item in self.manga_list:
            self.content_grid.removeWidget(item)
            item.deleteLater()
        self.manga_list.clear()

    @catch_exception
    def update_content(self):
        size = self.size().width() // self.column_count
        [item.set_size(size) for item in self.manga_list]

    @catch_exception
    def is_content_empy(self):
        if len(self.manga_list) != 0 and self.is_empty_label is not None:
            self.content_grid.removeWidget(self.is_empty_label)
            self.is_empty_label = None
        if len(self.manga_list) == 0 and self.is_empty_label is None:
            self.is_empty_label = QLabel("Ничего не найдено")
            self.content_grid.addWidget(self.is_empty_label)