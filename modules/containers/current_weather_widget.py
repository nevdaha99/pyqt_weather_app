from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ..image import ImageWidget


class CurrentWeatherWidget(QFrame):
    def __init__(
        self,
        city: str,
        weather: str,
        temperature: int,
        max_temperature: int,
        min_temperature: int,
        image,
    ):
        super().__init__()

        self.setFixedSize(390, 303)

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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        self.location_image = ImageWidget(16, 16, "dark_track.png")
        location_label = QLabel("Поточна позиція")
        location_top_widget = QWidget()
        location_top_layout = QHBoxLayout(location_top_widget)
        location_top_layout.setContentsMargins(0, 0, 0, 0)
        location_top_layout.setSpacing(16)
        location_top_layout.addWidget(self.location_image)
        location_top_layout.addWidget(location_label)
        location_top_layout.addStretch()
        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setFixedHeight(1)
        self.line.setStyleSheet("background-color: rgba(255, 255, 255, 51)")
        location_widget = QWidget()
        location_layout = QVBoxLayout(location_widget)
        location_layout.setContentsMargins(0, 0, 0, 0)
        location_layout.setSpacing(16)
        location_widget.setFixedSize(358, 30)
        location_layout.addWidget(location_top_widget)
        location_layout.addWidget(self.line)

        self.city_label = QLabel(city)
        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_label.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
        """)
        city_widget = QWidget()
        city_layout = QHBoxLayout(city_widget)
        city_layout.setSpacing(16)
        city_layout.addWidget(self.city_label)

        self.image_label = ImageWidget(250, 250, image)
        self.image_label.setStyleSheet("""
            background: transparent;
            margin-top: -150px;
            margin-left: -40px;
        """)
        self.temperature_label = QLabel(f"{temperature}°")
        self.temperature_label.setStyleSheet("""
            font-size: 70px;
            font-weight: bold;
        """)
        temp_widget = QWidget()
        temp_layout = QHBoxLayout(temp_widget)
        temp_widget.setFixedSize(270, 87)
        temp_layout.setContentsMargins(0, 0, 0, 0)

        temp_layout.addWidget(
            self.image_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        temp_layout.addWidget(
            self.temperature_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.weather_label = QLabel(weather)
        self.weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)
        self.min_max_label = QLabel(
            f"Макс.:{max_temperature}°, мін.:{min_temperature}°"
        )
        self.min_max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.min_max_label.setStyleSheet("font-size: 16px;")
        weather_widget = QWidget()
        weather_layout = QVBoxLayout(weather_widget)
        weather_layout.setContentsMargins(0, 0, 0, 0)
        weather_layout.setSpacing(10)
        weather_layout.addWidget(self.weather_label)
        weather_layout.addWidget(self.min_max_label)

        layout.addWidget(location_widget)

        layout.addWidget(
            city_widget,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        layout.addWidget(
            temp_widget,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        layout.addWidget(
            weather_widget,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

    def update_weather_data(self, data: dict):
        self.city_label.setText(data["city"])
        self.temperature_label.setText(f"{data['temperature']}°")
        self.weather_label.setText(data["weather"])

        self.min_max_label.setText(
            f"Макс.:{data['max_temperature']}°, "
            f"мін.:{data['min_temperature']}°"
        )

        self.image_label.set_image(data["image"])

    def change_theme(self, is_dark: bool):
        if is_dark:
            background_color = "rgba(0, 0, 0, 0.2)"
            text_color = "white"
            line_color = "rgba(255, 255, 255, 51)"
            self.location_image.set_image("dark_track.png")

        else:
            background_color = "rgba(255, 255, 255, 0.4)"
            text_color = "black"
            line_color = "rgba(0, 0, 0, 51)"
            self.location_image.set_image("light_track.png")

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
            self.setFixedSize(390, 303)

        elif size == "1440x1024":
            self.setFixedSize(464, 338)

        elif size == "1512x982":
            self.setFixedSize(486, 331)

        elif size == "1728x1117":
            self.setFixedSize(553, 352)
