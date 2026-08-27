from PyQt6.QtWidgets import *

from modules.containers.settings_modal import SettingsModal

from ..image import ImageWidget


class SettingsConteiner(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = ImageWidget(16, 16, "dark_settings.png")
        self.settings_label = QLabel("Налаштування")
        self.settings_label.setStyleSheet("background: transparent")
        self.settings.setStyleSheet("background: transparent")
        settings_layout = QHBoxLayout(self)
        settings_layout.setContentsMargins(8, 0, 8, 0)
        settings_layout.setSpacing(5)
        settings_layout.addWidget(self.settings)
        settings_layout.addWidget(self.settings_label)
        self.setFixedSize(144, 36)
        self.setStyleSheet(
            "background-color: rgba(0,0,0,0.2);border-radius: 8px"
        )
        self.modal = SettingsModal()

    def mousePressEvent(self, event):
        self.modal.show()

    def change_theme(self, is_dark: bool):
        if is_dark:
            self.settings.set_image("dark_settings.png")
            self.settings_label.setStyleSheet(
                "background: transparent; color: white;"
            )

        else:
            self.settings.set_image("light_settings.png")
            self.settings_label.setStyleSheet(
                "background: transparent; color: black;"
            )

    def update_lang(self, lang):
        if lang == "ua":
            self.settings_label.setText("Налаштування")
        else:
            self.settings_label.setText("Settings")
