from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import *

from ..image import ImageWidget
from ..utils.get_weather import get_weather_data, get_weather_data_by_coords
from ..utils.saving_config import get_config, save_config
from .tracked_city import TrackedCity

config = get_config()
list_city = config["list_city"]
selected = config["selected_city"]
is_dark = config["is_dark"]
image_pack = config["image_pack"]
size = config["size"]


class SidePanel(QWidget):
    city_selected = pyqtSignal(dict)
    theme_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.setFixedWidth(370)

        self.left_layout = QVBoxLayout(self)
        self.left_layout.setSpacing(10)
        self.left_layout.setContentsMargins(20, 20, 20, 20)
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.pack = image_pack
        self.is_dark = is_dark
        self.lang = config["language"]

        self.theme = ImageWidget(
            52,
            24,
            "moon.png" if self.is_dark else "sun.png",
        )
        self.theme.mousePressEvent = self.change_theme_icon

        self.left_layout.addWidget(
            self.theme,
            alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
        )
        self.added_city = []
        self.city_widgets = []
        for city in list_city:
            self.add_city(city, False)
        self.apply_theme()

    def add_city(self, city, saving=True):
        if city in self.added_city:
            return
        temp, temp_min, temp_max, description, time_zone, time, icon = (
            get_weather_data(city, self.lang)
        )
        if temp == None:
            return
        city_element = TrackedCity(
            city=city,
            time=time,
            weather=description,
            temperature=temp,
            max_temperature=temp_max,
            min_temperature=temp_min,
            icon=icon,
            image=f"icons/main/{self.pack}/{icon}.png",
            selected=city == config["selected_city"],
            layout=self.left_layout,
            list_city=self.added_city,
        )

        city_element.city_selected.connect(self.city_selected.emit)
        self.added_city.append(city)
        self.city_widgets.append(city_element)
        self.left_layout.addWidget(city_element)
        if saving:
            city_element.mousePressEvent(None)

    def add_city_by_coords(self, lat: float, lon: float, saving=True):
        (
            city,
            temp,
            temp_min,
            temp_max,
            description,
            time_zone,
            time,
            icon,
        ) = get_weather_data_by_coords(lat, lon)

        if city is None or temp is None:
            return

        if city in self.added_city:
            return

        city_element = TrackedCity(
            city=city,
            time=time,
            weather=description,
            temperature=temp,
            max_temperature=temp_max,
            min_temperature=temp_min,
            icon=icon,
            image=f"icons/main/{self.pack}/{icon}.png",
            selected=city == config["selected_city"],
            layout=self.left_layout,
            list_city=self.added_city,
        )

        city_element.city_selected.connect(self.city_selected.emit)

        self.added_city.append(city)
        self.city_widgets.append(city_element)
        self.left_layout.addWidget(city_element)

        if saving:
            city_element.mousePressEvent(None)

    def change_theme_icon(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return

        self.is_dark = not self.is_dark

        self.apply_theme()

        current_config = get_config()

        save_config(
            current_config["list_city"],
            current_config["selected_city"],
            self.is_dark,
            size,
            current_config["image_pack"],
            self.lang,
        )

        self.theme_changed.emit(self.is_dark)

    def remove_city(self, city_name: str):
        for city_widget in self.city_widgets[:]:
            if city_widget.city == city_name:
                self.left_layout.removeWidget(city_widget)
                self.city_widgets.remove(city_widget)
                city_widget.deleteLater()
                break

        if city_name in self.added_city:
            self.added_city.remove(city_name)

    def apply_theme(self):
        if self.is_dark:
            self.theme.set_image("moon.png")
        else:
            self.theme.set_image("sun.png")

        for city_widget in self.city_widgets:
            city_widget.change_theme(self.is_dark)

    def change_size(self, size: str):
        if size == "1200x800":
            self.setFixedSize(370, 800)

        elif size == "1440x1024":
            self.setFixedSize(434, 1024)

        elif size == "1512x982":
            self.setFixedSize(453, 982)

        elif size == "1728x1117":
            self.setFixedSize(510, 1117)

    def update_pack(self, pack_name):
        self.pack = pack_name

        for city_widget in self.city_widgets:
            icon = city_widget.weather_data["image"].split("/")[-1]

            city_widget.update_image(f"icons/main/{self.pack}/{icon}")

    def update_lang(self, lang):
        self.lang = lang
        for city_widget in self.city_widgets:
            city_widget.update_language(lang)

    def select_city(self, city_name: str):
        if not city_name:
            return

        for city_widget in self.city_widgets:
            if city_widget.city == city_name:
                city_widget.mousePressEvent(None)
                break
