import cv2
import os
from PyQt5.QtCore import QThread
# https://chel-center.ru/python-yfc/2021/05/27/chtenie-i-zapis-video-s-ispolzovaniem-opencv/


class ThreadProcessFrames(QThread):
    # путь до папки с кадрами из видео
    dir_path = ''

    # путь до видео
    source = ''

    def run(self):
        file_count = 0
        # Создаем объект захвата видео, в этом случае мы читаем видео из файла
        par = self.source[self.source.find('videos'):]
        vid_capture = cv2.VideoCapture(f'{par}')
        if not vid_capture.isOpened():
            return

        # создаем путь до ккадров
        self.dir_path = f'{self.source[:-4]}'
        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)

        print('start get frames of video')
        while 1:
            # Метод vid_capture.read() возвращают кортеж,
            # первым элементом является логическое значение, а вторым - кадр
            ret, frame = vid_capture.read()
            if not ret:
                break
            if file_count % 24 == 0:
                frame = cv2.resize(frame, (960, 720))
                cv2.imwrite(f'{self.dir_path}/{int(file_count/24)}.jpeg', frame)
                # data_img.append(frame)
            file_count += 1
        print('end get frames of video')
        # Освободить объект захвата видео
        vid_capture.release()
        cv2.destroyAllWindows()
        # for el in self.data_img:
        #     cv2.imshow('Look', el)
        #     cv2.waitKey(60)
