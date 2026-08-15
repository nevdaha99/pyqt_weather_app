from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from modules.image import ImageWidget
from modules.utils.graphic import get_graphic


class GraphicForecast(QFrame):
    def __init__(self, city_name):
        super().__init__()
        self.setFixedSize(788, 197)
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
        main_layout = QVBoxLayout(self)
        self.forecast_label = QLabel("Прогноз на 5 днів")
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(8)
        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setFixedHeight(1)
        self.line.setStyleSheet("background-color: rgba(255, 255, 255, 51)")
        main_layout.addWidget(self.forecast_label)
        main_layout.addWidget(self.line)

        graphic_frame = QFrame()
        graphic_layout = QHBoxLayout(graphic_frame)
        graphic_frame.setStyleSheet("background-color: transparent")
        graphic_layout.setContentsMargins(0, 0, 0, 0)
        graphic_frame.setFixedSize(755, 106)
        graphic_layout.setSpacing(6)
        column_frame = QFrame()
        column_frame.setFixedSize(725, 106)
        self.column_layout = QHBoxLayout(column_frame)
        self.grid = ImageWidget(725, 106, "grid.png")
        self.column_layout.setContentsMargins(0, 0, 0, 0)
        self.column_layout.setSpacing(3)
        scale_frame = QFrame()
        self.scale_layout = QVBoxLayout(scale_frame)
        scale_frame.setFixedSize(22, 106)
        self.scale_layout.setContentsMargins(0, 0, 0, 0)

        stack = QWidget()
        stack.setFixedSize(725, 106)
        stack_layout = QStackedLayout(stack)
        stack_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        stack_layout.addWidget(column_frame)
        stack_layout.addWidget(self.grid)

        graphic_layout.addWidget(stack)
        graphic_layout.addWidget(scale_frame)
        main_layout.addWidget(graphic_frame)

        min_temp, list_height = get_graphic(city_name)
        self.add_graphic(min_temp, list_height)

    def add_graphic(self, min_temp, list_height):
        for i in range(8):
            temp = (min_temp + 35) - i * 5
            label = QLabel(f"{temp}°")
            label.setStyleSheet("font-size: 10px")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.scale_layout.addWidget(label)
        for height in list_height:
            column = QFrame()
            column.setFixedHeight(height)
            column.setStyleSheet("""
                    background: qlineargradient(
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1,
                        stop: 0 #FFDF56,
                        stop: 1 #87CEFA
                    );
                    border-radius: 0;
                """)

            self.column_layout.addWidget(
                column,
                alignment=Qt.AlignmentFlag.AlignBottom,
            )

    def update_graphic(self, data: dict):
        city_name = data["city"]
        while self.scale_layout.count():
            item = self.scale_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        while self.column_layout.count():
            item = self.column_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        min_temp, list_height = get_graphic(city_name)
        self.add_graphic(min_temp, list_height)

    def change_theme(self, is_dark: bool):
        if is_dark:
            background_color = "rgba(0, 0, 0, 0.2)"
            text_color = "white"
            line_color = "rgba(255, 255, 255, 51)"

        else:
            background_color = "rgba(255, 255, 255, 0.4)"
            text_color = "black"
            line_color = "rgba(0, 0, 0, 51)"

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

        self.grid.setStyleSheet("background: transparent;")

    def change_size(self, size: str):
        if size == "1200x800":
            self.setFixedSize(788, 197)

        elif size == "1440x1024":
            self.setFixedSize(943, 215)

        elif size == "1512x982":
            self.setFixedSize(990, 211)

        elif size == "1728x1117":
            self.setFixedSize(1130, 222)
