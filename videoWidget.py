from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog, QGridLayout, QFrame, QCheckBox
from FramesOfVideo import ThreadProcessFrames
from CameraCalibration import ThreadProcessCalibration


class Widget(QWidget):
    video_or_image = True
    show_chess = False
    dir_path = ''

    def __init__(self):
        super().__init__()
        self.setStyleSheet('''
                    border: 1px solid black;
                ''')
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.label_video = QLabel()
        self.layout.addWidget(self.label_video, 0, 0, 1, 2)

        self.btn_choice = QPushButton("Выбрать видео")
        # self.btn_choice.setObjectName('btn_choice')
        self.btn_choice.clicked.connect(self.choice_video)
        self.layout.addWidget(self.btn_choice, 6, 0)

        self.btn_load = QPushButton("Загрузить видео")
        self.btn_load.setObjectName('btn_load')
        self.btn_load.clicked.connect(self.load_video)
        self.layout.addWidget(self.btn_load, 7, 0)

        self.btn_choice_frames = QPushButton("Выбрать кадры")
        # self.btn_choice_frames.setObjectName('btn_choice_frames')
        self.btn_choice_frames.clicked.connect(self.choice_frames)
        self.layout.addWidget(self.btn_choice_frames, 8, 0)

        self.btn_start = QPushButton("Начать калибровку")
        # self.btn_start.setObjectName('btn_start')
        self.btn_start.clicked.connect(self.start_calibration)
        self.layout.addWidget(self.btn_start, 7, 1)

        self.check_box = QCheckBox('Визуализировать углы?')
        # self.check_box.setObjectName('check_box')
        self.check_box.stateChanged.connect(self.show_chessboard)
        self.layout.addWidget(self.check_box, 8, 1)

        # блкирование кнопок
        self.block_btn()
        self.btn_choice.setEnabled(True)

        # многопоточность приложения
        self.thread_process_get_frames = ThreadProcessFrames(self)
        self.thread_process_calibration = ThreadProcessCalibration()

    # блкирование кнопок выбора кадров, калибровки и визуализации углов
    def block_btn(self):
        self.btn_choice.setEnabled(False)
        self.btn_choice_frames.setEnabled(False)
        self.btn_start.setEnabled(False)
        self.btn_load.setEnabled(False)
        self.check_box.setEnabled(False)

    # выбор видео
    def choice_video(self):
        options = QFileDialog.Options()
        self.PATH_TO_VIDEO, _ = QFileDialog.getOpenFileName(self,
                                                            "QFileDialog.getOpenFileName()", "",
                                                            "Videos (*.avi);;",
                                                            options=options)
        if self.PATH_TO_VIDEO:
            # блкирование кнопок
            self.block_btn()
            # разблокирование кнопки загрузки видео
            self.btn_choice.setEnabled(True)
            self.btn_load.setEnabled(True)

            self.thread_process_get_frames.source = self.PATH_TO_VIDEO

    # загрузка видео (сохранение кадров видео в папку по пути dir_path)
    def load_video(self):
        self.thread_process_get_frames.finished.connect(self.on_finished)
        self.thread_process_get_frames.start()
        # блокируем кнопки на время выполнения
        self.block_btn()

    # разблокирование кнопок
    @QtCore.pyqtSlot()
    def on_finished(self):
        self.btn_choice.setEnabled(True)
        self.btn_load.setEnabled(True)
        self.btn_choice_frames.setEnabled(True)
        self.btn_start.setEnabled(True)
        self.check_box.setEnabled(True)

    def choice_frames(self):
        options = QFileDialog.Options()
        self.files, _ = QFileDialog.getOpenFileNames(self,
                                                     "QFileDialog.getOpenFileNames()",
                                                     self.dir_path,
                                                     "Images (*.jpeg);;",
                                                     options=options)
        if self.files:
            self.video_or_image = False

    def start_calibration(self):
        if self.video_or_image:
            self.thread_process_calibration.source_path = self.dir_path
            self.thread_process_calibration.show_chess = self.show_chess
        else:
            self.thread_process_calibration.source_path = self.dir_path
            self.thread_process_calibration.source = self.files
            self.thread_process_calibration.video = self.video_or_image
            self.thread_process_calibration.show_chess = self.show_chess

        # запуск в отдельном потоке
        self.thread_process_calibration.finished.connect(self.on_finished)
        self.thread_process_calibration.start()
        # блкирование кнопок всех кнопок
        self.block_btn()

    def show_chessboard(self, state):
        self.show_chess = (state == Qt.Checked)
        print(self.show_chess)
