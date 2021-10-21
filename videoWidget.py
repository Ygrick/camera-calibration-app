import os
import sys
import numpy as np
import cv2
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog, QGridLayout, QFrame
from PyQt5.QtGui import QImage, QPixmap


class ThreadOpenCV(QThread):
    changePixmap = pyqtSignal(QImage)
    running = False
    video_set = False

    def __init__(self):
        super().__init__()

    def check_video_set(self):
        return self.video_set

    def set_path_video(self, source):
        self.source = source
        self.video_set = True
        self.running = True

    def run(self):
        print('start')

        cap = cv2.VideoCapture(self.source)

        self.running = True

        while self.running:
            ret, frame = cap.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w

                image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                image = image.scaled(480, 360, Qt.KeepAspectRatio)

                self.changePixmap.emit(image)

        cap.release()
        print('stop')

    def stop(self):
        self.running = False


# QtWidgets.QMainWindow
class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = ThreadOpenCV()
        self.layout = QGridLayout()
        self.setStyleSheet('''
            border: 1px solid black;
        ''')

        self.label_video = QLabel()
        self.layout.addWidget(self.label_video, 0, 0, 1, 2)

        self.btn_start = QPushButton("PLAY")
        self.btn_start.clicked.connect(self.playVideo)
        self.layout.addWidget(self.btn_start, 6, 0)

        self.btn_stop = QPushButton("STOP")
        self.btn_stop.clicked.connect(self.stopVideo)
        self.layout.addWidget(self.btn_stop, 7, 0)

        self.btn_file = QPushButton("FILE")
        self.btn_file.clicked.connect(self.open_file)
        self.layout.addWidget(self.btn_file, 6, 1)

        self.btn_save = QPushButton("SAVE")
        self.btn_save.clicked.connect(self.save_file)
        self.layout.addWidget(self.btn_save, 7, 1)

        self.setLayout(self.layout)

    def save_file(self):
        pass
        # if self.PATH_TO_VIDEO:
        #     with open(f'{self.PATH_TO_VIDEO}', "w") as f:
        #         f.write(self.PATH_TO_VIDEO)

    def open_file(self):
        options = QFileDialog.Options()
        self.PATH_TO_VIDEO, _ = QFileDialog.getOpenFileName(self,
                                                            "QFileDialog.getOpenFileName()", "",
                                                            "Videos (*.avi);;All Files (*)",
                                                            options=options)
        self.thread.set_path_video(self.PATH_TO_VIDEO)
        self.thread.changePixmap.connect(self.setImage)

    def playVideo(self):
        if self.thread.check_video_set():
            self.thread.start()
        else:
            pass

    def stopVideo(self):
        if self.thread.check_video_set():
            self.thread.running = False
        else:
            pass

    def setImage(self, image):
        self.label_video.setPixmap(QPixmap.fromImage(image))

