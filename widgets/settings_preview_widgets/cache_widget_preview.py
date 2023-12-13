from utils.decorators import catch_exception
from utils.file_manager import FileManager
from widgets.settings_preview_widgets.settings_preview_widget import SettingsPreviewWidget


class CachePreviewWidget(SettingsPreviewWidget):

    def __init__(self):
        super().__init__()

        self.icon_path = r"\cache.svg"
        self.file_manager = FileManager()

        self.setup()

    @catch_exception
    def setup(self):
        self.setup_ui()

    @catch_exception
    def setup_ui(self):
        self.ui.titleLabel.setText("Кэш приложения")
        temp_size = self.file_manager.get_temp_size()
        self.ui.descriptionLabel.setText(f"Занимаемая память: {temp_size}")
        self.setProperty('is_set', 0)
        self.set_icon(self.icon_path)