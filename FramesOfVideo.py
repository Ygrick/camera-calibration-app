import cv2
import os
import numpy as np

# https://chel-center.ru/python-yfc/2021/05/27/chtenie-i-zapis-video-s-ispolzovaniem-opencv/
def frames_of_video(source):
    file_count = 0
    # data_img = []
    # Создаем объект захвата видео, в этом случае мы читаем видео из файла
    vid_capture = cv2.VideoCapture(source)
    dirPath = f'E:/GitHub/camera-calibration-app/videos/calibrate/images{source[9:-4]}'
    print(dirPath)
    if not os.path.isdir(dirPath):
        os.mkdir(dirPath)
    if not vid_capture.isOpened():
        return
    while 1:
        # Метод vid_capture.read() возвращают кортеж,
        # первым элементом является логическое значение, а вторым - кадр
        ret, frame = vid_capture.read()
        if not ret:
            break
        if file_count % 24 == 0:
            frame = cv2.resize(frame, (960, 720))
            cv2.imwrite(f'{dirPath}/{int(file_count/24)}.jpg', frame)
            # data_img.append(frame)
        file_count += 1

    # Освободить объект захвата видео
    vid_capture.release()
    cv2.destroyAllWindows()
    return
    # for el in self.data_img:
    #     cv2.imshow('Look', el)
    #     cv2.waitKey(60)
