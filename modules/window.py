from PyQt6.QtWidgets import *

from .app import app


class Window(QMainWindow):
    def __init__(self, width, height, title):
        super().__init__()
        screen_width = app.primaryScreen().size().width()
        screen_height = app.primaryScreen().size().height()
        center_x = (screen_width - width) // 2
        center_y = (screen_height - height) // 2
        self.setGeometry(center_x, center_y, width, height)
        self.setWindowTitle(title)
        # self.setStyleSheet("""
        #     QFrame {
        #         background: qlineargradient(
        #             x1:1, y1:0,
        #             x2:0, y2:1,
        #             stop:0 #FFDF56,
        #             stop:1 #87CEFA
        #         );
        #     }
        # """)
        self.change_bg_color("01d")

    def change_size(self, size: str):
        width, height = map(int, size.split("x"))
        screen_width = app.primaryScreen().size().width()
        screen_height = app.primaryScreen().size().height()
        center_x = (screen_width - width) // 2
        center_y = (screen_height - height) // 2
        self.setGeometry(center_x, center_y, width, height)
        self.setFixedSize(width, height)

    def change_bg_color(self, icon):
        backgrounds = {
            # Ясно, день
            "01d": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #FFDF56,
                    stop: 1 #87CEFA
                )
            """,
            # Ясно, ночь
            "01n": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #8A2BE2,
                    stop: 1 #191970
                )
            """,
            # Малооблачно, день
            "02d": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #FFDF56,
                    stop: 1 #87CEFA
                )
            """,
            # Малооблачно, ночь
            "02n": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #8A2BE2,
                    stop: 1 #191970
                )
            """,
            # Облачно
            "03d": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #FFD27F,
                    stop: 1 #C0C0C0
                )
            """,
            "03n": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #8A2BE2,
                    stop: 1 #191970
                )
            """,
            # Пасмурно
            "04d": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #808080,
                    stop: 1 #5DADE2
                )
            """,
            "04n": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #8A2BE2,
                    stop: 1 #191970
                )
            """,
            # Дождь
            "09d": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #4A4A4A,
                    stop: 1 #5DADE2
                )
            """,
            "09n": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #4A4A4A,
                    stop: 1 #5DADE2
                )
            """,
            # Сильный дождь
            "10d": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #4A4A4A,
                    stop: 1 #5DADE2
                )
            """,
            "10n": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #4A4A4A,
                    stop: 1 #5DADE2
                )
            """,
            # Гроза
            "11d": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #4A4A4A,
                    stop: 1 #5DADE2
                )
            """,
            "11n": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #4A4A4A,
                    stop: 1 #5DADE2
                )
            """,
            # Снег
            "13d": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #FFFFFF,
                    stop: 1 #B0C4DE
                )
            """,
            "13n": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #AEBED0,
                    stop: 1 #B0C4DE
                )
            """,
            # Туман
            "50d": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #C5C5C5,
                    stop: 1 #777777
                )
            """,
            "50n": """
                qlineargradient(
                    x1: 1, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #707070,
                    stop: 1 #383838
                )
            """,
        }

        background = backgrounds.get(icon, backgrounds["01d"])

        self.setStyleSheet(f"""
            QMainWindow {{
                background: {background};
            }}
        """)

    def closeEvent(self, event):
        container = self.centralWidget()

        if container and hasattr(container, "settings"):
            container.settings.modal.close()

        event.accept()


window = Window(width=1200, height=800, title="app")
