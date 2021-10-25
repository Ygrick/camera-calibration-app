import numpy as np
import cv2
from FramesOfVideo import ThreadProcessFrames
import glob
from PyQt5.QtCore import QThread


class ThreadProcessCalibration(QThread):
    source_path = ''
    source = []
    video = True
    show_chess = False
    def run(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*7, 3), np.float32)
        objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        if self.video:
            print('video calibration mode selected')
            source_path = self.source_path[self.source_path.find('videos'):]
            images = glob.iglob(f'{source_path}/*')
            # print(f'videos/calibrate/{source_path[7:]}.avi')
            # print(f'{source_path[:]}.avi')
        else:
            print('image calibration mode selected')
            thread_get_frames = ThreadProcessFrames()
            thread_get_frames.dir_path = self.source_path
            images = thread_get_frames.run()
        # glob.glob("E:/GitHub/camera-calibration-app/videos/calibrate/images1_20211006-160404_1_167/*.jpg")

        for frame in images:
            image = cv2.imread(frame)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)

            # If found, add object points, image points (after refining them)
            if ret:
                objpoints.append(objp)
                imgpoints.append(corners)
                if self.show_chess:
                    # возможность визуализации найденных углов шахматного паттерна
                    corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                    # Draw and display the corners
                    cv2.drawChessboardCorners(image, (7, 6), corners2, ret)
                    cv2.imshow('img', image)
                    # cv2.imwrite(_путь_, image)
                    cv2.waitKey(50)
        print('end add img and obj points')
        if imgpoints:
            print('start calibration video')
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
            vid_capture = cv2.VideoCapture(f'{source_path}.avi')
            if not vid_capture.isOpened():
                return
            width, height = 960, 720
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            writer = cv2.VideoWriter(f'videos/calibrate/{source_path[7:]}.avi', fourcc, 20, (width, height))
            new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))
            x, y, w, h = roi
            while 1:
                ret, frame = vid_capture.read()
                if not ret:
                    break
                # undistort
                frame = cv2.resize(frame, (960, 720))
                frame = cv2.undistort(frame, mtx, dist, None, new_camera_mtx)
                writer.write(frame)
            print(f'end calibration video, check path: videos/calibrate/{source_path[7:]}.avi')
            vid_capture.release()
        cv2.destroyAllWindows()
