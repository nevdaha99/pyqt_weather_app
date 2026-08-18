from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
)

from modules.utils.saving_config import get_config, save_config

config = get_config()
is_dark = config["is_dark"]


class TrackedCity(QFrame):
    city_selected = pyqtSignal(dict)

    def __init__(
        self,
        city: str,
        time: str,
        weather: str,
        temperature: int,
        max_temperature: int,
        min_temperature: int,
        image,
        selected: bool,
        layout,
        list_city,
    ):
        super().__init__()
        self.weather_data = {
            "city": city,
            "weather": weather,
            "temperature": temperature,
            "max_temperature": max_temperature,
            "min_temperature": min_temperature,
            "image": image,
        }
        self.setFixedHeight(100)
        self.list_sity = list_city
        self.city = city
        self.image_path = image

        self.setStyleSheet("""
            background-color: transparent;
            QLabel {
                color: white;
                background: transparent;
            }
        """)
        if selected:
            self.setStyleSheet("""
                background-color: rgba(0,0,0,0.2);
                border-radius: 8px;
                QLabel {
                    color: white;
                    background-color: transparent;
                }
            """)
        self.left_layout = layout

        layout = QGridLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(2)

        self.city_label = QLabel(city)

        self.time_label = QLabel(time)

        self.weather_label = QLabel(weather)

        self.temperature_label = QLabel(f"{temperature}°")

        self.temperature_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        )

        self.min_max_label = QLabel(
            f"Макс.:{max_temperature}°, мін.:{min_temperature}°"
        )
        self.min_max_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(self.city_label, 0, 0)
        layout.addWidget(self.time_label, 1, 0)
        layout.addWidget(self.weather_label, 2, 0)

        layout.addWidget(self.temperature_label, 0, 1, 2, 1)
        layout.addWidget(self.min_max_label, 2, 1)
        self.change_theme(True)

    def mousePressEvent(self, event: QtGui.QMouseEvent | None) -> None:
        for i in range(self.left_layout.count()):
            item = self.left_layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, TrackedCity):
                widget.setStyleSheet("background-color: transparent")
        self.setStyleSheet("""
            background-color: rgba(0,0,0,0.2);
            border-radius: 8px;
            QLabel {
                color: white;
                background-color: transparent;
            }
        """)
        save_config(self.list_sity, self.weather_data["city"], is_dark)
        self.city_selected.emit(self.weather_data)

    def change_theme(self, is_dark: bool):
        if is_dark:
            city_color = "#FFFFFF"
            text_color = "rgba(255, 255, 255, 204)"
        else:
            city_color = "rgba(44, 44, 44, 230)"
            text_color = "rgba(44, 44, 44, 179)"

        self.city_label.setStyleSheet(f"""
            color: {city_color};
            font-size: 22px;
            font-weight: bold;
            background-color: transparent;
        """)

        self.temperature_label.setStyleSheet(f"""
            color: {text_color};
            font-size: 44px;
            font-weight: bold;
            background-color: transparent;
        """)

        self.time_label.setStyleSheet(f"""
            color: {text_color};
            font-size: 13px;
            background-color: transparent;
        """)

        self.weather_label.setStyleSheet(f"""
            color: {text_color};
            font-size: 13px;
            background-color: transparent;
        """)

        self.min_max_label.setStyleSheet(f"""
            color: {text_color};
            font-size: 13px;
            background-color: transparent;
        """)

    def update_image(self, image):
        self.image_path = image
        self.weather_data["image"] = image
