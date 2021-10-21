import numpy as np
import cv2 as cv
from FramesOfVideo import frames_of_video


def camera_calibration(source):
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = frames_of_video(source)

    for fname in images:
        gray = cv.cvtColor(fname, cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (7, 6), None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)
            # corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            # cv.drawChessboardCorners(fname, (7, 6), corners2, ret)
            # cv.imshow('img', fname)
            # cv.waitKey(50)

    cv.destroyAllWindows()
    if imgpoints:
        print('hello')
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        img = cv.imread('videos/left14.jpg')
        h,  w = img.shape[:2]
        new_camera_mtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

        # undistort
        dst = cv.undistort(img, mtx, dist, None, new_camera_mtx)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv.imwrite('videos/calibresult2.png', dst)


camera_calibration('videos/+-1_20211006-160404_1_167.avi')