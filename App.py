import os
import sys
import numpy as np
import cv2
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog, QGridLayout, QFrame
from PyQt5.QtGui import QImage, QPixmap
from videoWidget import Widget

# отсюда брал
# https://question-it.com/questions/3247143/kak-zapustit-video-v-kontejnere-pyqt

# отсюда надо брать
# https://stackoverflow.com/questions/39303008/load-an-opencv-video-frame-by-frame-using-pyqt

# проигрыватель
# https://pythonprogramminglanguage.com/pyqt5-video-widget/

# gridlayout
# https://realpython.com/python-pyqt-layout/

# документация по PyQt
# https://doc.qt.io/qtforpython/index.html


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(60, 60,  1280, 720)

        self.layout = QGridLayout()
        self.widget0 = Widget()
        self.widget1 = Widget()
        self.widget2 = Widget()
        self.widget3 = Widget()
        self.widget4 = Widget()
        self.widget5 = Widget()
        self.widget = QWidget()

        self.init_ui()

    def init_ui(self):
        self.layout.addWidget(self.widget0, 0, 0)
        self.layout.addWidget(self.widget1, 0, 1)
        self.layout.addWidget(self.widget2, 0, 2)
        self.layout.addWidget(self.widget3, 1, 0)
        self.layout.addWidget(self.widget4, 1, 1)
        self.layout.addWidget(self.widget5, 1, 2)

        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    mw = App()
    mw.show()

    app.exec()