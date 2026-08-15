import os

from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
)

from modules.image import ImageWidget
from modules.utils.get_weather import get_forecast_data


class Forecast(QFrame):
    def __init__(self, city_name):
        super().__init__()
        self.is_dark = True
        self.setFixedSize(788, 157)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(0,0,0,0.2);
                border-radius: 15px;
            }

            QLabel {
                background: transparent;
                color: white;
            }
        """)
        weather_list, description = get_forecast_data(city_name)
        main_layout = QVBoxLayout(self)
        self.forecast_label = QLabel(description)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(8)
        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setFixedHeight(1)
        self.line.setStyleSheet("background-color: rgba(255, 255, 255, 51)")
        main_layout.addWidget(self.forecast_label)
        main_layout.addWidget(self.line)

        self.control_frame = QFrame()
        self.control_frame.setFixedSize(756, 82)
        control_layout = QHBoxLayout(self.control_frame)
        control_layout.setContentsMargins(0, 0, 0, 0)
        self.control_frame.setStyleSheet("background-color: transparent")
        control_layout.setSpacing(24)
        self.left_button = ImageWidget(16, 16, "dark_left.png")
        self.right_button = ImageWidget(16, 16, "dark_right.png")
        main_layout.addWidget(self.control_frame)

        self.left_button.mousePressEvent = lambda e: (
            scroll.horizontalScrollBar().setValue(
                scroll.horizontalScrollBar().value() - 62
            )
        )

        self.right_button.mousePressEvent = lambda e: (
            scroll.horizontalScrollBar().setValue(
                scroll.horizontalScrollBar().value() + 62
            )
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedSize(676, 82)
        scroll.setStyleSheet("background-color: transparent")
        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        forecast_frame = QFrame()
        self.forecast_layout = QHBoxLayout(forecast_frame)
        self.forecast_layout.setSpacing(17)
        forecast_frame.setFixedHeight(82)
        forecast_frame.setStyleSheet("background-color: transparent")
        scroll.setWidget(forecast_frame)
        control_layout.addWidget(self.left_button)
        control_layout.addWidget(scroll)
        control_layout.addWidget(self.right_button)
        self.add_forecast(weather_list)

    def add_forecast(self, weather_list):
        theme = "dark" if self.is_dark else "light"
        self.weather_list = weather_list
        for weather in self.weather_list:
            frame = QFrame()
            frame.setFixedSize(45, 82)
            frame.setContentsMargins(0, 0, 0, 0)
            frame.setStyleSheet("background-color: transparent")
            layout = QVBoxLayout(frame)
            layout.setSpacing(10)
            time = QLabel(weather["time"])
            temp = QLabel(str(weather["temp"]) + "°")
            icon = QSvgWidget(
                os.path.abspath(
                    __file__
                    + f"/../../../images/icons/{theme}/{weather['icon']}.svg"
                )
            )
            icon.setFixedSize(24, 24)
            layout.addWidget(time)
            layout.addWidget(icon)
            layout.addWidget(temp)
            self.forecast_layout.addWidget(frame)

    def update_forecast(self, data: dict):
        city_name = data["city"]
        while self.forecast_layout.count():
            item = self.forecast_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.weather_list, description = get_forecast_data(city_name)
        self.forecast_label.setText(description)
        self.add_forecast(self.weather_list)

    def change_theme(self, is_dark: bool):
        self.is_dark = is_dark
        while self.forecast_layout.count():
            item = self.forecast_layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        self.add_forecast(self.weather_list)

        if is_dark:
            background_color = "rgba(0, 0, 0, 0.2)"
            text_color = "white"
            line_color = "rgba(255, 255, 255, 51)"

            self.left_button.set_image("dark_left.png")
            self.right_button.set_image("dark_right.png")

        else:
            background_color = "rgba(255, 255, 255, 0.4)"
            text_color = "black"
            line_color = "rgba(0, 0, 0, 51)"

            self.left_button.set_image("light_left.png")
            self.right_button.set_image("light_right.png")

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {background_color};
                border-radius: 15px;
            }}

            QLabel {{
                background: transparent;
                color: {text_color};
            }}
        """)

        self.line.setStyleSheet(f"background-color: {line_color};")

    def change_size(self, size: str):
        if size == "1200x800":
            self.setFixedSize(788, 157)
            self.control_frame.setFixedSize(756, 82)

        elif size == "1440x1024":
            self.setFixedSize(943, 183)
            self.control_frame.setFixedSize(911, 108)

        elif size == "1512x982":
            self.setFixedSize(990, 178)
            self.control_frame.setFixedSize(958, 103)

        elif size == "1728x1117":
            self.setFixedSize(1130, 194)
            self.control_frame.setFixedSize(1098, 119)
