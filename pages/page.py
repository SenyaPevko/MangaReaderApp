import os

from PyQt6.QtWidgets import QWidget


class Page(QWidget):
    closed_icon_path = rf"{os.getcwd()}\icons\side_menu\settings_closed.svg"
    selected_icon_path = rf"{os.getcwd()}\icons\side_menu\settings_selected.svg"
    def update(self):
        pass