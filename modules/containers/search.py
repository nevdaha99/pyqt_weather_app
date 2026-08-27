from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import *

from ..image import ImageWidget


class Search(QFrame):
    city_added = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setStyleSheet(
            "background-color: rgba(0,0,0,0.2);border-radius: 8px"
        )
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        self.add_widget = QWidget()
        self.add_widget.setFixedHeight(36)
        self.add_widget.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_widget.hide()
        self.add_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 8px;
            }

            QLabel {
                color: white;
                background: transparent;
            }
        """)
        add_layout = QHBoxLayout(self.add_widget)
        add_layout.setContentsMargins(8, 0, 8, 0)
        add_layout.setSpacing(4)
        self.add_icon = QLabel("⊕")
        self.add_icon.setStyleSheet("font-size: 30px;")
        self.add_text = QLabel("Додати")
        self.add_text.setStyleSheet("font-size: 14px;")
        self.add_icon.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.add_text.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        add_layout.addWidget(self.add_icon)
        add_layout.addWidget(self.add_text)
        self.add_widget.mousePressEvent = self.add_city_clicked
        main_layout.addWidget(self.add_widget)

        self.search_frame = QFrame()
        self.search_frame.setFixedSize(261, 36)
        self.search_frame.setStyleSheet("background-color: transparent")
        search_layout = QHBoxLayout(self.search_frame)
        search_layout.setContentsMargins(8, 0, 8, 0)
        search_layout.setSpacing(6)
        self.search_icon = ImageWidget(20, 17, "dark_search.png")
        search_layout.addWidget(self.search_icon)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Пошук")
        self.search.setFixedHeight(22)
        self.search.textChanged.connect(self.on_text_changed)
        self.search.returnPressed.connect(self.search_city)
        search_layout.addWidget(self.search)
        main_layout.addWidget(self.search_frame)

    def on_text_changed(self, text: str):
        self.add_widget.setVisible(bool(text.strip()))

    def add_city_clicked(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.search_city()

    def search_city(self):
        city = self.search.text().strip().capitalize()
        if not city:
            return
        self.city_added.emit(city)
        self.search.clear()

    def change_theme(self, is_dark: bool):
        if is_dark:
            self.setStyleSheet(
                "background-color: rgba(0,0,0,0.2);border-radius: 8px"
            )
            self.add_widget.setStyleSheet("""
                    QWidget {
                        background-color: rgba(0, 0, 0, 0.2);
                        border-radius: 8px;
                    }
                """)
            self.add_icon.setStyleSheet("""
                    font-size: 30px;
                    color: white;
                    background: transparent;
                """)
            self.add_text.setStyleSheet("""
                    font-size: 14px;
                    color: white;
                    background: transparent;
                """)
            self.search.setStyleSheet("""
                    QLineEdit {
                        background: transparent;
                        color: white;
                        border: none;
                    }
                """)

            self.search_icon.set_image("dark_search.png")

        else:
            self.setStyleSheet(
                "background-color: rgba(255, 255, 255, 0.4);border-radius: 8px"
            )
            self.add_widget.setStyleSheet("""
                    QWidget {
                        background-color: rgba(0, 0, 0, 0.2);
                        border-radius: 8px;
                    }
                """)
            self.add_icon.setStyleSheet("""
                    font-size: 30px;
                    color: black;
                    background: transparent;
                """)
            self.add_text.setStyleSheet("""
                    font-size: 14px;
                    color: black;
                    background: transparent;
                """)
            self.search.setStyleSheet("""
                    QLineEdit {
                        background: transparent;
                        color: black;
                        border: none;
                    }
                """)

            self.search_icon.set_image("light_search.png")

    def update_lang(self, lang):
        if lang == "ua":
            self.add_text.setText("Додати")
            self.search.setPlaceholderText("Пошук")
        else:
            self.add_text.setText("Add")
            self.search.setPlaceholderText("Search")
