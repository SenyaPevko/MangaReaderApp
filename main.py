import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from app import App
from Views.windows.main_window import MainWindow


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor)
    app = App(sys.argv)
    with open("Views/ui/styles/widgets.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
