from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QLayout

from utils.decorators import catch_exception


def get_partly_colored_text(uncolored_part, colored_part, color):
    widget = QWidget()
    widget_text = QLabel(f'{uncolored_part}<span style="color:#{color};">{colored_part} %s</span>')
    widget_layout = QHBoxLayout()
    widget_layout.addWidget(widget_text)
    widget_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
    widget.setLayout(widget_layout)
    return widget


@catch_exception
def set_icon(icon_path: str, button: QLabel, icon_max_size: QSize):
    button.setMaximumSize(icon_max_size)
    icon_pixmap = QPixmap(icon_path)
    pixmap = icon_pixmap.scaled(button.maximumSize(), Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation)
    button.setPixmap(pixmap)
