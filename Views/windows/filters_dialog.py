from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFrame, QGridLayout, QCheckBox, QSizePolicy, \
    QDialogButtonBox, QPushButton

from utils.decorators import catch_exception


class FiltersDialog(QDialog):
    discarded = pyqtSignal()

    def __init__(self, genres: dict):
        super().__init__()
        self.columns_count = 6
        self.genres = genres
        self.genres_check_boxes: list[QCheckBox] = []

        self.verticalLayout = QVBoxLayout(self)
        self.filtersFrame = QFrame(parent=self)
        self.verticalLayout_2 = QVBoxLayout(self.filtersFrame)
        self.gridLayout = QGridLayout()
        self.buttonBox = QDialogButtonBox(parent=self)

        self.setup_ui()

    @catch_exception
    def setup_ui(self):
        self.setObjectName("filtersDialog")
        self.resize(400, 300)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.verticalLayout.setObjectName("verticalLayout")
        self.filtersFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.filtersFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.filtersFrame.setObjectName("filtersFrame")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.filtersFrame)

        self.set_button_box()
        self.set_genres()

    @catch_exception
    def set_button_box(self):
        accept_button = QPushButton("Применить")
        accept_button.setDefault(True)
        accept_button.clicked.connect(self.accept)
        discard_button = QPushButton("Отменить")
        discard_button.setDefault(True)
        discard_button.clicked.connect(self.discard)
        close_button = QPushButton("Закрыть")
        close_button.setDefault(True)
        close_button.clicked.connect(self.reject)

        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(size_policy)
        self.buttonBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.addButton(accept_button, QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(discard_button, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(close_button, QDialogButtonBox.ButtonRole.RejectRole)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

    @catch_exception
    def set_genres(self):
        raw_count = 0
        column_count = 0

        for genre in self.genres:
            check_box = QCheckBox(parent=self.filtersFrame)
            size_policy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(check_box.sizePolicy().hasHeightForWidth())
            check_box.setSizePolicy(size_policy)
            check_box.setTristate(True)
            check_box.setText(genre)
            self.genres_check_boxes.append(check_box)
            self.gridLayout.addWidget(check_box, raw_count, column_count, 1, 1)

            column_count += 1
            if column_count == self.columns_count - 1:
                column_count = 0
                raw_count += 1

    @catch_exception
    def get_selected_genres(self):
        return self.get_genres_by_state(Qt.CheckState.Checked)

    @catch_exception
    def get_removed_genres(self):
        return self.get_genres_by_state(Qt.CheckState.PartiallyChecked)

    @catch_exception
    def get_genres_by_state(self, state: Qt.CheckState):
        selected_genres = []
        for genre in self.genres_check_boxes:
            if genre.checkState() == state:
                selected_genres.append(self.genres[genre.text()])

        return selected_genres

    @catch_exception
    def discard(self, args):
        self.close()
        for genre_check_box in self.genres_check_boxes:
            genre_check_box.setCheckState(Qt.CheckState.Unchecked)
        self.discarded.emit()
