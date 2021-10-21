import cv2
import numpy as np

# https://chel-center.ru/python-yfc/2021/05/27/chtenie-i-zapis-video-s-ispolzovaniem-opencv/
def frames_of_video(source):
    file_count = 0
    data_img = []
    # Создаем объект захвата видео, в этом случае мы читаем видео из файла
    vid_capture = cv2.VideoCapture(source)
    if not vid_capture.isOpened():
        print("Ошибка открытия видеофайла")
    while vid_capture.isOpened():
        # Метод vid_capture.read() возвращают кортеж,
        # первым элементом является логическое значение, а вторым - кадр
        ret, frame = vid_capture.read()
        file_count += 1
        if file_count % 20 == 0:
            frame = cv2.resize(frame, (960, 720))
            # data_img = np.append(data_img, img)
            data_img.append(frame)
            # writefile = 'Resources/Image_sequence/is42_{0:04d}.jpg'.format(file_count)
            # cv2.imwrite(writefile, frame)
            # cv2.waitKey(1)
        if not ret:
            break
    # Освободить объект захвата видео
    vid_capture.release()
    cv2.destroyAllWindows()
    return data_img
    # for el in self.data_img:
    #     cv2.imshow('Look', el)
    #     cv2.waitKey(60)
