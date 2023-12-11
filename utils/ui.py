from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QLayout


def get_partly_colored_text(uncolored_part, colored_part, color):
    widget = QWidget()
    widget_text = QLabel(f'{uncolored_part}<span style="color:#{color};">{colored_part} %s</span>')
    widget_layout = QHBoxLayout()
    widget_layout.addWidget(widget_text)
    widget_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
    widget.setLayout(widget_layout)
    return widget
