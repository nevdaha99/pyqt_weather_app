import os

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import *


class ImageWidget(QLabel):
    def __init__(self, width, height, name):
        super().__init__()
        self.width_image = width
        self.height_image = height
        path = os.path.abspath(__file__ + f"/../../images/{name}")
        image = Image.open(path)
        image_qt = ImageQt(image)
        image = QImage(image_qt)
        pixmap = QPixmap(image).scaled(width, height)
        self.setFixedSize(width, height)
        self.setPixmap(pixmap)
        self.setStyleSheet("background-color: transparent")

    def set_image(self, name):
        path = os.path.abspath(__file__ + f"/../../images/{name}")
        image = Image.open(path)
        image_qt = ImageQt(image)
        image = QImage(image_qt)
        pixmap = QPixmap(image).scaled(
            self.width_image,
            self.height_image,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.setPixmap(pixmap)

    def set_image_size(self, width, height):
        self.width_image = width
        self.height_image = height
        self.setFixedSize(width, height)

    def change_size(self, width, height):
        self.set_image_size(width, height)
        self.setPixmap(
            self.pixmap().scaled(
                width,
                height,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
