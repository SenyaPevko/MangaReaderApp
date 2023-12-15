import sys
from PyQt6.QtCore import Qt, QFile, QTextStream
from PyQt6.QtWidgets import QApplication
from windows.main_window import MainWindow
# pyuic6.exe .\main_window2.ui -o .\main_window_ui2.py


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


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor)
    app = App(sys.argv)
    with open("ui/styles/widgets.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
