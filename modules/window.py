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
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:1, y1:0,
                    x2:0, y2:1,
                    stop:0 #FFDF56,
                    stop:1 #87CEFA
                );
            }
        """)

    def change_size(self, size: str):
        width, height = map(int, size.split("x"))
        screen_width = app.primaryScreen().size().width()
        screen_height = app.primaryScreen().size().height()
        center_x = (screen_width - width) // 2
        center_y = (screen_height - height) // 2
        self.setGeometry(center_x, center_y, width, height)


window = Window(width=1200, height=800, title="app")
