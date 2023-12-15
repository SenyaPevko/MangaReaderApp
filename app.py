from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtWidgets import QApplication


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.set_style()

    def get_style(self):
        widgets = self.read_file(QFile("ui/styles/widgets.qss"))
        style = widgets
        return style

    def read_file(self, file: QFile):
        file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        stream = QTextStream(file)
        return stream.readAll()

    def set_style(self):
        self.setStyleSheet(self.get_style())