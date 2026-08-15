from datetime import datetime, timezone

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from modules.utils.get_weather import get_weather_data

from ..image import ImageWidget


class TimeWidget(QFrame):
    city = pyqtSignal(str)

    def __init__(self, time_zone):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
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
        current_time = datetime.now(timezone.utc) + time_zone

        self.days = {
            0: "Понеділок",
            1: "Вівторок",
            2: "Середа",
            3: "Четвер",
            4: "П'ятниця",
            5: "Субота",
            6: "Неділя",
        }

        self.today_label = QLabel("Сьогодні")
        self.today_label.setStyleSheet("font-size: 14px;")
        today_widget = QWidget()
        today_layout = QVBoxLayout(today_widget)
        today_widget.setFixedSize(358, 30)
        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setFixedHeight(1)
        self.line.setStyleSheet("background-color: rgba(255, 255, 255, 51)")
        today_layout.setContentsMargins(0, 0, 0, 0)
        today_layout.setSpacing(16)
        today_layout.addWidget(self.today_label)
        today_layout.addWidget(self.line)

        self.day_label = QLabel(self.days[current_time.weekday()])
        self.day_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)
        self.date_label = QLabel(current_time.strftime("%d.%m.%Y"))
        self.date_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)
        date_widget = QWidget()
        date_layout = QHBoxLayout(date_widget)
        date_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_layout.setSpacing(16)
        date_layout.addWidget(self.day_label)
        date_layout.addStretch()
        date_layout.addWidget(self.date_label)

        self.clock_image = ImageWidget(168, 168, "time.png")
        self.clock_image.setStyleSheet("""
                background-color: rgba(0,0,0,0.2);
                border-radius: 80px;
                QLabel {
                    color: white;
                    background-color: transparent;
                }
            """)

        self.time_label = QLabel(current_time.strftime("%H:%M"))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("""
            color: white;
            font-size: 29px;
            font-weight: bold;
            background: transparent;
        """)
        self.time_label.setFixedSize(110, 50)
        clock_widget = QWidget()
        clock_widget.setFixedSize(168, 168)
        clock_layout = QGridLayout(clock_widget)
        clock_layout.setContentsMargins(0, 0, 0, 0)
        clock_layout.setSpacing(0)
        clock_layout.addWidget(
            self.clock_image, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )

        clock_layout.addWidget(
            self.time_label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(today_widget)

        layout.addWidget(date_widget)

        layout.addWidget(clock_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def update_city(self, weather_data):
        city = weather_data["city"]
        temp, temp_min, temp_max, description, time_zone, time, icon = (
            get_weather_data(city)
        )
        current_time = datetime.now(timezone.utc) + time_zone
        self.date_label.setText(current_time.strftime("%d.%m.%Y"))
        self.time_label.setText(time)
        self.day_label.setText(self.days[current_time.weekday()])

    def change_theme(self, is_dark: bool):
        if is_dark:
            background_color = "rgba(0, 0, 0, 0.2)"
            text_color = "white"
            line_color = "rgba(255, 255, 255, 51)"
            clock_background = "rgba(0, 0, 0, 0.2)"
        else:
            background_color = "rgba(255, 255, 255, 0.4)"
            text_color = "black"
            line_color = "rgba(0, 0, 0, 51)"
            clock_background = "rgba(255, 255, 255, 0.25)"

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

        self.clock_image.setStyleSheet(f"""
            background-color: {clock_background};
            border-radius: 84px;
        """)

        self.time_label.setStyleSheet(f"""
            color: {text_color};
            font-size: 29px;
            font-weight: bold;
            background: transparent;
        """)

    def change_size(self, size: str):
        if size == "1200x800":
            self.setFixedSize(390, 303)

        elif size == "1440x1024":
            self.setFixedSize(464, 338)

        elif size == "1512x982":
            self.setFixedSize(486, 331)

        elif size == "1728x1117":
            self.setFixedSize(553, 352)
