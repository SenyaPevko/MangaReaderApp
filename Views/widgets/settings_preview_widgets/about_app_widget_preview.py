from utils import app_info
from utils.decorators import catch_exception
from Views.widgets.settings_preview_widgets.settings_preview_widget import SettingsPreviewWidget


class AboutAppWidgetPreview(SettingsPreviewWidget):

    def __init__(self):
        super().__init__()

        self.icon_path = r"\about_app.svg"

        self.setup()

    @catch_exception
    def setup(self):
        self.setup_ui()

    @catch_exception
    def setup_ui(self):
        self.ui.titleLabel.setText("О приложении")
        self.ui.descriptionLabel.setText(f"Версия: {app_info.APP_VERSION}")
        self.setProperty('is_set', 0)
        self.set_icon(self.icon_path)