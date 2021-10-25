from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog, QGridLayout, QFrame, QCheckBox
from FramesOfVideo import ThreadProcessFrames
from CameraCalibration import ThreadProcessCalibration


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.choice_video = True
        self.show_chess = False
        self.layout = QGridLayout()
        self.setStyleSheet('''
            border: 1px solid black;
        ''')

        # многопоточность приложения
        self.thread_process_get_frames = ThreadProcessFrames()
        self.thread_process_calibration = ThreadProcessCalibration()

        self.label_video = QLabel()
        self.layout.addWidget(self.label_video, 0, 0, 1, 2)

        self.btn_load = QPushButton("Загрузить видео")
        self.btn_load.clicked.connect(self.load_video)
        self.layout.addWidget(self.btn_load, 6, 0)

        self.btn_choice_frames = QPushButton("Выбрать кадры")
        self.btn_choice_frames.clicked.connect(self.choice_frames)

        self.btn_start = QPushButton("Начать калибровку")
        self.btn_start.clicked.connect(self.start_calibration)

        self.check_box = QCheckBox('Визуализировать углы?')
        self.check_box.stateChanged.connect(self.show_chessboard)

        # self.btn_save = QPushButton("SAVE")
        # self.btn_save.clicked.connect(self.save_file)
        # self.layout.addWidget(self.btn_save, 7, 1)

        self.setLayout(self.layout)

    def load_video(self):
        options = QFileDialog.Options()
        self.PATH_TO_VIDEO, _ = QFileDialog.getOpenFileName(self,
                                                            "QFileDialog.getOpenFileName()", "",
                                                            "Videos (*.avi);;",
                                                            options=options)
        if self.PATH_TO_VIDEO:
            print("efgj")
            self.thread_process_get_frames.start()
            print("eer")
            self.dir_path = self.thread_process_get_frames.frames_of_video(self.PATH_TO_VIDEO)
            self.layout.addWidget(self.btn_choice_frames, 7, 0)
            self.layout.addWidget(self.btn_start, 6, 1)
            self.layout.addWidget(self.check_box, 7, 1)

    def choice_frames(self):
        options = QFileDialog.Options()
        self.files, _ = QFileDialog.getOpenFileNames(self,
                                                     "QFileDialog.getOpenFileNames()",
                                                     self.dir_path,
                                                     "Images (*.jpeg);;",
                                                     options=options)
        if self.files:
            self.choice_video = False

    def start_calibration(self):
        self.thread_process_calibration.start()
        if self.choice_video:
            self.thread_process_calibration.camera_calibration(source_path=self.dir_path,
                                                               show_chess=self.show_chess)
        else:
            self.thread_process_calibration.camera_calibration(source_path=self.dir_path,
                                                               source=self.files,
                                                               video=self.choice_video,
                                                               show_chess=self.show_chess)

    def show_chessboard(self, state):
        self.show_chess = (state == Qt.Checked)
        print(self.show_chess)
