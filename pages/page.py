import os

from PyQt6.QtWidgets import QWidget

from utils.app_info import ICONS_PATH


class Page(QWidget):
    closed_icon_path = rf"{ICONS_PATH}\side_menu\settings_closed.svg"
    selected_icon_path = rf"{ICONS_PATH}\side_menu\settings_selected.svg"

    def update(self):
        pass
