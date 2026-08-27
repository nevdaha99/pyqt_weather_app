import io

import folium
from PyQt6.QtCore import QEvent, Qt, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import *

from modules.utils.saving_config import get_config, save_config

from ..app import app
from ..image import ImageWidget, QPixmap

config = get_config()
list_city = config["list_city"]
selected_city = config["selected_city"]
is_dark = config["is_dark"]
lang = config["language"]
check_list = []
ua_language = config["settings_language"]["ua"]
en_language = config["settings_language"]["en"]
size = config["size"]
image_pack = config["image_pack"]


class SettingsModal(QWidget):
    coordinates_changed = pyqtSignal(float, float)
    city_deleted = pyqtSignal(str)
    size_app = pyqtSignal(str)
    pack_changed = pyqtSignal(str)
    lang_changed = pyqtSignal(str)
    selected_city = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        width = 790
        height = 688
        screen_width = app.primaryScreen().size().width()
        screen_height = app.primaryScreen().size().height()
        center_x = (screen_width - width) // 2
        center_y = (screen_height - height) // 2
        self.setGeometry(center_x, center_y, width, height)
        self.setStyleSheet("background-color: #363636")
        self.setWindowTitle("Налаштування")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.current_language = lang
        self.language = ua_language
        self.window_size = size
        self.image_pack = image_pack

        settings_layout = QVBoxLayout(self)
        settings_layout.setSpacing(34)
        settings_layout.setContentsMargins(24, 24, 24, 24)
        title_frame = QFrame()
        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(ua_language["title"])
        self.title.setStyleSheet("color: white;font-size: 24px")
        close = ImageWidget(24, 24, "close.png")
        close.mousePressEvent = self.close_event
        title_layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignTop)
        title_layout.addStretch()
        title_layout.addWidget(close, alignment=Qt.AlignmentFlag.AlignTop)
        settings_layout.addWidget(
            title_frame,
            alignment=Qt.AlignmentFlag.AlignTop,
        )

        button_style = """
        QPushButton {
            background-color: transparent;
            border: none;
            border-radius: 4px;
            color: #737373;
            font-size: 16px;
            text-align: left;
            padding: 10px 12px;
        }

        QPushButton:hover {
            background-color: #303030;
            color: white;
        }

        QPushButton:pressed {
            background-color: #262626;
        }

        QPushButton:checked {
            background-color: #2B2B2B;
            color: white;
    }
    """

        content_frame = QFrame()
        content_layout = QHBoxLayout(content_frame)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(0, 0, 0, 0)
        left_panel = QFrame()
        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.setSpacing(0)
        self.search_city_button = QPushButton(
            ua_language["search_city_button"]
        )
        self.app_size_button = QPushButton(ua_language["app_size_button"])
        self.language_button = QPushButton(ua_language["language_button"])
        self.image_list_button = QPushButton(ua_language["image_list_button"])
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for button in (
            self.search_city_button,
            self.app_size_button,
            self.language_button,
            self.image_list_button,
        ):
            button.setCheckable(True)
            button.setStyleSheet(button_style)
            self.button_group.addButton(button)
            left_panel_layout.addWidget(button)
        self.search_city_button.setChecked(True)

        left_panel_layout.addWidget(self.search_city_button)
        left_panel_layout.addWidget(self.app_size_button)
        left_panel_layout.addWidget(self.language_button)
        left_panel_layout.addWidget(self.image_list_button)
        content_layout.addWidget(
            left_panel, alignment=Qt.AlignmentFlag.AlignTop
        )
        settings_layout.addWidget(
            content_frame, alignment=Qt.AlignmentFlag.AlignTop
        )
        settings_layout.addStretch()

        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setFixedSize(1, 578)
        line.setStyleSheet("background-color: rgba(255, 255, 255, 51)")
        content_layout.addWidget(line)

        search_city_frame = QFrame()
        search_city_layout = QVBoxLayout(search_city_frame)
        search_city_layout.setContentsMargins(0, 0, 0, 0)
        search_city_layout.setSpacing(24)

        coordinat_frame = QFrame()
        coordinat_layout = QHBoxLayout(coordinat_frame)
        coordinat_layout.setSpacing(16)
        coordinat_layout.setContentsMargins(0, 0, 0, 0)

        control_frame = QFrame()
        control_layout = QVBoxLayout(control_frame)
        content_layout.setSpacing(24)
        control_layout.setContentsMargins(0, 0, 0, 0)

        search_city_layout.addWidget(coordinat_frame)
        coordinat_layout.addWidget(
            control_frame, alignment=Qt.AlignmentFlag.AlignTop
        )
        # поиск по координатам
        self.search_title = QLabel(ua_language["search_city_button"])
        self.search_title.setStyleSheet("font-size: 18px")
        self.coordinat_title = QLabel(ua_language["coordinat_title"])
        self.coordinat_title.setStyleSheet("font-size: 14px")
        self.coordinat_input = QLineEdit()
        self.coordinat_input.setPlaceholderText(ua_language["coordinat_input"])
        self.coordinat_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: none;
                border-radius: 6px;
                padding: 0 12px;
                color: #222;
                font-size: 15px;
            }

            QLineEdit::placeholder {
                color: #6F7280;
            }

            QLineEdit:focus {
                border: 1px solid #4C8BF5;
            }
        """)
        self.coordinat_input.setFixedSize(239, 32)
        self.save_coordinate = QPushButton(ua_language["save_button"])
        self.save_coordinate.clicked.connect(self.search_coords)
        self.save_coordinate.setStyleSheet("""
            QPushButton {
                background-color: #0F0F0F;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                padding: 6px;
            }

            QPushButton:hover:enabled {
                background-color: #1A1A1A;
            }

            QPushButton:pressed:enabled {
                background-color: #050505;
            }

            QPushButton:disabled {
                background-color: #434343;
                color: #8B8B8B;
            }
        """)
        self.save_coordinate.setFixedSize(105, 38)
        self.save_coordinate.setEnabled(False)
        self.coordinat_input.textChanged.connect(self.update_save_button)

        control_layout.addWidget(self.search_title)
        control_layout.addSpacing(24)
        control_layout.addWidget(self.coordinat_title)
        control_layout.addWidget(self.coordinat_input)
        control_layout.addWidget(self.save_coordinate)
        control_layout.addStretch()

        self.coords = (48.4667, 35.0167)

        map = folium.Map(location=self.coords)
        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(289, 256)
        coordinat_layout.addWidget(
            self.web_view, alignment=Qt.AlignmentFlag.AlignTop
        )
        data = io.BytesIO()
        map.save(data, close_file=False)
        self.web_view.setHtml(data.getvalue().decode())

        added_city_frame = QFrame()
        added_city_layout = QVBoxLayout(added_city_frame)
        added_city_frame.setFixedSize(544, 197)
        added_city_layout.setSpacing(12)
        added_city_layout.setContentsMargins(0, 0, 0, 0)
        added_city_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.added_city_label = QLabel(ua_language["added_city_label"])
        self.added_city_label.setStyleSheet("font-size: 18px")
        added_city_layout.addWidget(self.added_city_label)
        search_city_layout.addWidget(added_city_frame)

        self.scrolll = QScrollArea()
        self.scrolll.setFixedSize(544, 160)
        self.scrolll.setWidgetResizable(True)
        self.scrolll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scrolll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.list_city_frame = QFrame()
        self.list_city_layout = QVBoxLayout(self.list_city_frame)
        self.list_city_layout.setContentsMargins(0, 0, 0, 0)
        self.list_city_layout.setSpacing(0)
        self.list_city_frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 55);
            border-radius: 8px;
        """)
        self.add_found_city()

        self.scrolll.setWidget(self.list_city_frame)

        added_city_layout.addWidget(self.scrolll)
        self.pages = QStackedWidget()
        self.pages.addWidget(search_city_frame)
        # смена размеров приложения
        self.size_page = QWidget()
        size_layout = QVBoxLayout(self.size_page)
        size_layout.setContentsMargins(8, 0, 0, 0)
        size_layout.setSpacing(0)
        size_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.size_title = QLabel(ua_language["size_title"])
        self.size_title.setStyleSheet("""
            color: white;
            font-size: 18px;
            background-color: transparent;
        """)
        self.size_title.setFixedHeight(30)

        size_layout.addWidget(self.size_title)
        size_layout.addSpacing(8)

        self.size_1200 = QRadioButton("1200x800")
        self.size_1440 = QRadioButton("1440x1024")
        self.size_1512 = QRadioButton("1512x982")
        self.size_1728 = QRadioButton("1728x1117")

        radio_style = """
            QRadioButton {
                color: white;
                font-size: 14px;
                background-color: transparent;
                spacing: 8px;
            }

            QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px;
                border: 1px solid white;
                background-color: transparent;
            }

            QRadioButton::indicator:checked {
                background-color: white;
                border: 1px solid white;
            }

            QRadioButton::indicator:unchecked {
                background-color: transparent;
                border: 1px solid white;
            }
        """

        self.size_buttons = QButtonGroup(self)
        self.size_buttons.setExclusive(True)

        for button in (
            self.size_1200,
            self.size_1440,
            self.size_1512,
            self.size_1728,
        ):
            button.setStyleSheet(radio_style)
            button.setFixedHeight(33)

            self.size_buttons.addButton(button)
            size_layout.addWidget(button)
        self.size_1200.setChecked(True)

        size_layout.addSpacing(12)

        self.save_size_button = QPushButton(ua_language["save_button"])
        self.save_size_button.setFixedSize(105, 38)
        self.save_size_button.setEnabled(False)
        self.save_size_button.clicked.connect(self.get_selected_size)

        self.save_size_button.setStyleSheet("""
            QPushButton {
                background-color: #0F0F0F;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }

            QPushButton:hover:enabled {
                background-color: #1A1A1A;
            }

            QPushButton:pressed:enabled {
                background-color: #050505;
            }

            QPushButton:disabled {
                background-color: #434343;
                color: #8B8B8B;
            }
        """)
        self.size_buttons.buttonClicked.connect(
            lambda: self.save_size_button.setEnabled(True)
        )
        size_layout.addWidget(self.save_size_button)

        size_layout.addStretch()

        self.pages.addWidget(self.size_page)
        # язык приложения
        self.language_page = QWidget()
        language_layout = QVBoxLayout(self.language_page)
        language_layout.setContentsMargins(24, 20, 0, 0)
        language_layout.setSpacing(0)
        language_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.language_title = QLabel(ua_language["language_title"])
        self.language_title.setStyleSheet("font-size: 18px;")
        self.language_title.setFixedHeight(40)
        self.language_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: 400;
            }
        """)

        language_layout.addWidget(self.language_title)

        self.language_label = QLabel(ua_language["language_button"])
        self.language_label.setFixedHeight(35)
        self.language_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        language_layout.addWidget(self.language_label)

        self.language_combo = QComboBox()
        self.language_combo.setFixedSize(240, 32)

        self.language_combo.addItems(["Українська", "English"])

        self.language_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #222;
                border: none;
                border-radius: 5px;
                padding-left: 10px;
                font-size: 12px;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox QAbstractItemView {
                background-color: white;
                color: #222;
                selection-background-color: #e6e6e6;
                selection-color: #222;
                border: none;
            }
        """)

        language_layout.addWidget(self.language_combo)
        language_layout.addSpacing(24)
        self.language_save_button = QPushButton(ua_language["save_button"])
        self.language_save_button.setFixedSize(105, 38)
        self.language_save_button.setStyleSheet("""
            QPushButton {
                background-color: #0F0F0F;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #1A1A1A;
            }

            QPushButton:pressed {
                background-color: #050505;
            }
        """)
        language_layout.addWidget(self.language_save_button)
        self.language_save_button.clicked.connect(self.save_language)
        self.pages.addWidget(self.language_page)

        # смена пака картинок
        self.images_page = QWidget()
        images_layout = QVBoxLayout(self.images_page)
        images_layout.setContentsMargins(0, 0, 0, 0)
        images_layout.setSpacing(0)
        images_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.images_title = QLabel(ua_language["image_list_button"])
        self.images_title.setFixedHeight(30)

        self.images_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                background-color: transparent;
            }
        """)

        images_layout.addWidget(self.images_title)
        images_layout.addSpacing(15)

        self.pack_group = QButtonGroup(self)
        self.pack_group.setExclusive(True)

        list1_header = QHBoxLayout()
        list1_header.setContentsMargins(0, 0, 0, 0)

        self.list1_title = QLabel(ua_language["list1_title"])
        self.list1_title.setFixedHeight(22)

        self.list1_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 15px;
                background-color: transparent;
            }
        """)

        self.pack1_radio = QRadioButton()
        self.pack1_radio.setChecked(True)
        self.pack1_radio.hide()

        self.pack_group.addButton(self.pack1_radio)

        list1_header.addWidget(self.list1_title)
        list1_header.addStretch()
        list1_header.addWidget(self.pack1_radio)

        images_layout.addLayout(list1_header)
        images_layout.addSpacing(10)

        self.list1_frame = QFrame()
        self.list1_frame.setFixedSize(490, 137)

        self.list1_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 55);
                border-radius: 6px;
            }
        """)
        self.list1_frame.installEventFilter(self)

        list1_layout = QHBoxLayout(self.list1_frame)
        list1_layout.setContentsMargins(15, 15, 15, 15)
        list1_layout.setSpacing(22)

        list1_images = [
            "images/icons/main/pack1/01d.png",
            "images/icons/main/pack1/02d.png",
            "images/icons/main/pack1/09d.png",
            "images/icons/main/pack1/03n.png",
            "images/icons/main/pack1/04n.png",
        ]

        for path in list1_images:
            image_frame = QFrame()
            image_frame.setFixedSize(74, 74)

            image_frame.setStyleSheet("""
                QFrame {
                    background-color: rgba(255, 255, 255, 0.18);
                    border-radius: 8px;
                }
            """)

            image_layout = QVBoxLayout(image_frame)
            image_layout.setContentsMargins(5, 5, 5, 5)
            image_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            image_label = QLabel()
            image_label.setFixedSize(64, 64)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            image_label.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)

            pixmap = QPixmap(path)

            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    150,
                    150,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                image_label.setPixmap(pixmap)

            image_layout.addWidget(image_label)
            list1_layout.addWidget(image_frame)

        images_layout.addWidget(self.list1_frame)

        images_layout.addSpacing(25)

        list2_header = QHBoxLayout()
        list2_header.setContentsMargins(0, 0, 0, 0)

        self.list2_title = QLabel(ua_language["list2_title"])
        self.list2_title.setFixedHeight(22)

        self.list2_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 15px;
                background-color: transparent;
            }
        """)

        self.pack2_radio = QRadioButton()
        self.pack2_radio.hide()

        self.pack_group.addButton(self.pack2_radio)

        list2_header.addWidget(self.list2_title)
        list2_header.addStretch()
        list2_header.addWidget(self.pack2_radio)

        images_layout.addLayout(list2_header)
        images_layout.addSpacing(10)

        self.list2_frame = QFrame()
        self.list2_frame.setFixedSize(490, 137)

        self.list2_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 55);
                border-radius: 6px;
            }
        """)
        self.list2_frame.installEventFilter(self)

        list2_layout = QHBoxLayout(self.list2_frame)
        list2_layout.setContentsMargins(15, 15, 15, 15)
        list2_layout.setSpacing(22)

        list2_images = [
            "images/icons/main/pack2/01d.png",
            "images/icons/main/pack2/02d.png",
            "images/icons/main/pack2/09d.png",
            "images/icons/main/pack2/03n.png",
            "images/icons/main/pack2/04n.png",
        ]
        for path in list2_images:
            image_frame = QFrame()
            image_frame.setFixedSize(74, 74)

            image_frame.setStyleSheet("""
                QFrame {
                    background-color: rgba(255, 255, 255, 0.18);
                    border-radius: 8px;
                }
            """)

            image_layout = QVBoxLayout(image_frame)
            image_layout.setContentsMargins(5, 5, 5, 5)
            image_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            image_label = QLabel()
            image_label.setFixedSize(64, 64)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            image_label.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)

            pixmap = QPixmap(path)

            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    65,
                    65,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                image_label.setPixmap(pixmap)

            image_layout.addWidget(image_label)
            list2_layout.addWidget(image_frame)

        images_layout.addWidget(self.list2_frame)

        images_layout.addSpacing(15)

        self.save_pack_button = QPushButton(ua_language["save_button"])
        self.save_pack_button.setFixedSize(105, 38)

        self.save_pack_button.setStyleSheet("""
            QPushButton {
                background-color: #0F0F0F;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #1A1A1A;
            }

            QPushButton:pressed {
                background-color: #050505;
            }
        """)

        self.save_pack_button.clicked.connect(self.save_selected_pack)

        images_layout.addWidget(self.save_pack_button)

        images_layout.addStretch()
        self.update_selected_pack()
        self.pages.addWidget(self.images_page)

        content_layout.addWidget(
            self.pages, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.search_city_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.app_size_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.language_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        self.image_list_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
        )
        self.pages.setCurrentIndex(0)

    def close_event(self, event):
        self.close()

    def search_coords(self):
        self.coords = self.get_coordinates()

        if self.coords is None:
            return

        latitude, longitude = self.coords
        self.coordinates_changed.emit(latitude, longitude)
        self.coords = self.coordinat_input.text().split(",")
        map = folium.Map(location=self.coords)
        data = io.BytesIO()
        map.save(data, close_file=False)
        self.web_view.setHtml(data.getvalue().decode())

    def update_save_button(self, text):
        self.save_coordinate.setEnabled(bool(text.strip()))

    def get_coordinates(self):
        text = self.coordinat_input.text().strip()

        try:
            latitude, longitude = map(float, text.split(","))
            return latitude, longitude

        except ValueError:
            return None

    def add_found_city(self, city_added=None):
        if city_added:
            city_label = QLabel(city_added)
            city_label.setStyleSheet("""
                background-color: transparent;
                color: white;
                font-size: 16px;
            """)
            city_label.setFixedHeight(20)
            frame = QFrame()
            layout = QHBoxLayout(frame)
            frame.setFixedSize(512, 32)
            frame.setStyleSheet("background-color: transparent")
            layout.setContentsMargins(24, 0, 0, 0)
            layout.setSpacing(8)
            delete_icon = ImageWidget(16, 16, "delete.png")
            delete_icon.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_icon.mousePressEvent = (
                lambda event, city_name=city_added, city_frame=frame: (
                    self.delete_city(city_name, city_frame)
                )
            )
            check_list.append(city_added)
            layout.addWidget(
                city_label, alignment=Qt.AlignmentFlag.AlignVCenter
            )
            layout.addStretch()
            layout.addWidget(delete_icon)
            self.list_city_layout.addWidget(frame)
            self.list_city_frame.setMinimumHeight(
                self.list_city_layout.count() * 32
            )
        for city in list_city:
            if city not in check_list:
                city_label = QLabel(city)
                city_label.setStyleSheet("""
                    background-color: transparent;
                    color: white;
                    font-size: 16px;
                """)
                city_label.setFixedHeight(20)
                frame = QFrame()
                layout = QHBoxLayout(frame)
                frame.setFixedSize(512, 32)
                frame.setStyleSheet("background-color: transparent")
                layout.setContentsMargins(24, 0, 0, 0)
                layout.setSpacing(8)
                delete_icon = ImageWidget(16, 16, "delete.png")
                delete_icon.setCursor(Qt.CursorShape.PointingHandCursor)
                delete_icon.mousePressEvent = (
                    lambda event, city_name=city, city_frame=frame: (
                        self.delete_city(city_name, city_frame)
                    )
                )
                check_list.append(city)
                layout.addWidget(
                    city_label, alignment=Qt.AlignmentFlag.AlignVCenter
                )
                layout.addStretch()
                layout.addWidget(delete_icon)
                self.list_city_layout.addWidget(frame)
                self.list_city_frame.setMinimumHeight(
                    self.list_city_layout.count() * 32
                )

    def delete_city(self, city_name: str, city_frame: QFrame):
        self.list_city_layout.removeWidget(city_frame)
        city_frame.deleteLater()
        config = get_config()
        selected_city = config["selected_city"]

        if city_name in list_city:
            list_city.remove(city_name)
        if city_name == selected_city:
            if list_city:
                selected_city = list_city[0]
            else:
                selected_city = ""
        self.selected_city.emit(selected_city)
        save_config(
            list_city,
            selected_city,
            is_dark,
            self.window_size,
            self.image_pack,
            lang,
        )
        self.city_deleted.emit(city_name)

    def get_selected_size(self):
        selected_button = self.size_buttons.checkedButton()
        if selected_button is None:
            return
        selected_size = selected_button.text()
        config = get_config()
        list_city = config["list_city"]
        selected_city = config["selected_city"]
        is_dark = config["is_dark"]
        image_pack = config["image_pack"]
        lang = config["language"]
        save_config(
            list_city,
            selected_city,
            is_dark,
            selected_size,
            image_pack,
            lang,
        )

        self.size_app.emit(selected_size)

    def save_selected_pack(self):
        config = get_config()
        lang = config["language"]
        if self.pack1_radio.isChecked():
            self.pack_changed.emit("pack1")
            save_config(
                list_city,
                selected_city,
                is_dark,
                self.window_size,
                "pack1",
                lang,
            )

        elif self.pack2_radio.isChecked():
            self.pack_changed.emit("pack2")
            save_config(
                list_city,
                selected_city,
                is_dark,
                self.window_size,
                "pack2",
                lang,
            )

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if obj == self.list1_frame:
                self.pack1_radio.setChecked(True)
                self.update_selected_pack()

            elif obj == self.list2_frame:
                self.pack2_radio.setChecked(True)
                self.update_selected_pack()

        return super().eventFilter(obj, event)

    def update_selected_pack(self):
        selected_style = """
            QFrame {
                background-color: rgba(0, 0, 0, 110);
                border-radius: 6px;
            }
        """

        normal_style = """
            QFrame {
                background-color: rgba(0, 0, 0, 55);
                border-radius: 6px;
            }
        """

        self.list1_frame.setStyleSheet(
            selected_style if self.pack1_radio.isChecked() else normal_style
        )

        self.list2_frame.setStyleSheet(
            selected_style if self.pack2_radio.isChecked() else normal_style
        )

    def save_language(self):
        language = self.language_combo.currentText()
        config = get_config()

        if language == "Українська":
            self.current_language = "ua"
        else:
            self.current_language = "en"

        config["language"] = self.current_language

        save_config(
            config["list_city"],
            config["selected_city"],
            config["is_dark"],
            config["size"],
            config["image_pack"],
            config["language"],
        )

        self.update_language()

    def update_language(self):
        if self.current_language == "ua":
            self.language = ua_language
            self.lang_changed.emit("ua")
        else:
            self.language = en_language
            self.lang_changed.emit("en")

        self.title.setText(self.language["title"])

        self.search_city_button.setText(self.language["search_city_button"])
        self.app_size_button.setText(self.language["app_size_button"])
        self.language_button.setText(self.language["language_button"])
        self.image_list_button.setText(self.language["image_list_button"])

        self.search_title.setText(self.language["search_city_button"])
        self.coordinat_title.setText(self.language["coordinat_title"])

        self.coordinat_input.setPlaceholderText(
            self.language["coordinat_input"]
        )

        self.save_coordinate.setText(self.language["save_button"])

        self.added_city_label.setText(self.language["added_city_label"])

        self.size_title.setText(self.language["size_title"])

        self.save_size_button.setText(self.language["save_button"])

        self.language_title.setText(self.language["language_title"])

        self.language_label.setText(self.language["language_button"])

        self.language_save_button.setText(self.language["save_button"])

        self.images_title.setText(self.language["image_list_button"])

        self.list1_title.setText(self.language["list1_title"])

        self.list2_title.setText(self.language["list2_title"])

        self.save_pack_button.setText(self.language["save_button"])
