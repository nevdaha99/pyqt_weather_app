import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
app = QApplication(sys.argv)
