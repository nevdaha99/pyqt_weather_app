from datetime import timedelta

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import *

from modules.containers.current_weather_widget import CurrentWeatherWidget
from modules.containers.forecast import Forecast
from modules.containers.graphic_forecast import GraphicForecast
from modules.utils.saving_config import get_config

from .containers.search import Search
from .containers.settings_conteiner import SettingsConteiner
from .containers.side_panel import SidePanel
from .containers.time_widget import TimeWidget
from .utils.get_weather import get_weather_data
from .window import window

config = get_config()
selected_city = config["selected_city"]
is_dark = config["is_dark"]
lang = config["language"]
pack = config["image_pack"]
size = config["size"]


class MainContainer(QFrame):
    size_changed = pyqtSignal(str)
    size_changed1 = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.side_panel = SidePanel()
        self.scroll_panel = QScrollArea()
        self.scroll_panel.setWidgetResizable(True)
        self.scroll_panel.setFixedSize(370, 800)
        self.scroll_panel.setStyleSheet("background-color: rgba(0,0,0,0.2)")
        self.scroll_panel.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_panel.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_panel.setWidget(self.side_panel)
        self.side_panel.theme_changed.connect(self.change_theme)

        self.right_frame = QFrame()
        self.right_frame.setStyleSheet("background-color: transparent;")
        self.right_frame.setFixedSize(828, 800)

        self.main_layout.addWidget(self.scroll_panel, 0)
        self.main_layout.addWidget(self.right_frame, 1)

        self.right_layout = QVBoxLayout(self.right_frame)
        self.right_layout.setContentsMargins(20, 20, 20, 20)
        self.right_layout.setSpacing(10)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.search = Search()
        self.header_frame = QFrame()
        self.header_frame.setFixedSize(788, 46)
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.settings = SettingsConteiner()
        self.settings.modal.coordinates_changed.connect(
            self.side_panel.add_city_by_coords
        )
        self.settings.modal.lang_changed.connect(self.settings.update_lang)
        self.settings.modal.lang_changed.connect(self.search.update_lang)
        self.settings.update_lang(lang)
        self.search.update_lang(lang)
        self.settings.modal.update_language()
        # self.settings.modal.selected_city.connect(self.change_selected_city)
        self.settings.modal.selected_city.connect(self.side_panel.select_city)

        self.settings.modal.city_deleted.connect(self.side_panel.remove_city)
        self.settings.modal.size_app.connect(self.size_changed.emit)
        self.settings.modal.size_app.connect(self.size_changed1.emit)
        self.settings.modal.pack_changed.connect(self.side_panel.update_pack)
        self.settings.modal.lang_changed.connect(self.side_panel.update_lang)
        self.side_panel.update_lang(lang)

        self.search.city_added.connect(self.settings.modal.add_found_city)

        header_layout.addWidget(self.settings)
        header_layout.addStretch(1)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.search.city_added.connect(self.side_panel.add_city)
        header_layout.addWidget(self.search)
        self.right_layout.addWidget(self.header_frame)

        temp, temp_min, temp_max, description, timezone, time, icon = (
            get_weather_data(selected_city, lang)
        )
        if not icon:
            icon = "01d"
        if not timezone:
            timezone = timedelta(seconds=0)
        window.change_bg_color(icon)
        self.pack = pack
        self.city = CurrentWeatherWidget(
            city=selected_city,
            weather=description,
            temperature=temp,
            max_temperature=temp_max,
            min_temperature=temp_min,
            image=f"icons/main/{self.pack}/{icon}.png",
            icon=icon,
        )
        self.city.update_pack(self.pack)
        self.settings.modal.pack_changed.connect(self.city.update_pack)
        self.main_weather_frame = QFrame()
        self.main_weather_frame.setFixedSize(788, 303)
        main_weather_layout = QHBoxLayout(self.main_weather_frame)
        main_weather_layout.setSpacing(10)
        main_weather_layout.setContentsMargins(0, 0, 0, 0)
        self.side_panel.city_selected.connect(self.city.update_weather_data)
        main_weather_layout.addWidget(
            self.city,
        )
        self.side_panel.city_selected.connect(self.update_background)
        self.settings.modal.lang_changed.connect(self.city.update_lang)
        self.city.update_lang(lang)
        self.time_widget = TimeWidget(timezone)
        self.side_panel.city_selected.connect(self.time_widget.update_city)
        self.settings.modal.lang_changed.connect(self.time_widget.update_lang)
        self.time_widget.update_lang(lang)
        main_weather_layout.addWidget(
            self.time_widget,
        )
        self.right_layout.addWidget(self.main_weather_frame)

        self.forecast_widget = Forecast(selected_city)
        self.side_panel.city_selected.connect(
            self.forecast_widget.update_forecast
        )
        self.settings.modal.lang_changed.connect(
            self.forecast_widget.update_lang
        )
        self.forecast_widget.update_lang(lang)
        self.right_layout.addWidget(
            self.forecast_widget, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        if selected_city:
            self.graphic_widget = GraphicForecast(selected_city)
        else:
            self.graphic_widget = GraphicForecast(None)
        self.side_panel.city_selected.connect(
            self.graphic_widget.update_graphic
        )
        self.settings.modal.lang_changed.connect(
            self.graphic_widget.update_lang
        )
        self.graphic_widget.update_lang(lang)
        self.right_layout.addWidget(
            self.graphic_widget, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.change_theme(is_dark)

    def change_theme(self, is_dark: bool):

        if is_dark:
            self.scroll_panel.setStyleSheet(
                "background-color: rgba(0, 0, 0, 0.2);"
            )

            self.right_frame.setStyleSheet("background-color: transparent;")

        else:
            self.scroll_panel.setStyleSheet(
                "background-color: rgba(255, 255, 255, 102);"
            )

            self.right_frame.setStyleSheet("background-color: transparent;")

        self.search.change_theme(is_dark)
        self.settings.change_theme(is_dark)
        self.city.change_theme(is_dark)
        self.time_widget.change_theme(is_dark)
        self.forecast_widget.change_theme(is_dark)
        self.graphic_widget.change_theme(is_dark)

    def change_size(self, size: str):
        if size == "1200x800":
            self.scroll_panel.setFixedSize(370, 800)
            self.right_frame.setFixedSize(828, 800)

            self.header_frame.setFixedSize(788, 46)
            self.main_weather_frame.setFixedSize(788, 303)

        elif size == "1440x1024":
            self.scroll_panel.setFixedSize(434, 1024)
            self.right_frame.setFixedSize(1006, 1024)

            self.header_frame.setFixedSize(966, 55)
            self.main_weather_frame.setFixedSize(966, 338)

        elif size == "1512x982":
            self.scroll_panel.setFixedSize(453, 982)
            self.right_frame.setFixedSize(1059, 982)

            self.header_frame.setFixedSize(1019, 55)
            self.main_weather_frame.setFixedSize(1019, 331)

        elif size == "1728x1117":
            self.scroll_panel.setFixedSize(510, 1117)
            self.right_frame.setFixedSize(1218, 1117)

            self.header_frame.setFixedSize(1178, 60)
            self.main_weather_frame.setFixedSize(1170, 352)

        self.side_panel.change_size(size)
        self.city.change_size(size)
        self.time_widget.change_size(size)
        self.forecast_widget.change_size(size)
        self.graphic_widget.change_size(size)

    def update_background(self, data):
        icon = data["icon"]
        window.change_bg_color(icon)

    def change_selected_city(self, city):
        if not city:
            return

        self.selected_city = city
        self.update_weather(city)


container = MainContainer()
container.size_changed.connect(window.change_size)
container.size_changed1.connect(container.change_size)
window.change_size(size)
container.change_size(size)
window.setCentralWidget(container)
