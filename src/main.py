import cv2
import numpy as np

from detection.Cube import Cube
from detection.Utils import Utils


def nothing(x):
    pass


def main():
    cap = cv2.VideoCapture(0)
    cap.open("http://192.168.144.236:8080/video")
    cv2.namedWindow("Cube")
    cv2.createTrackbar("MinHue", "Cube", 0, 255, nothing)
    # cv2.createTrackbar("MaxHue", "Cube", 9, 255, nothing)

    # cv2.createTrackbar("MinSat", "Cube", 99, 255, nothing)
    # cv2.createTrackbar("MaxSat", "Cube", 226, 255, nothing)

    # cv2.createTrackbar("MinVal", "Cube", 70, 255, nothing)
    # cv2.createTrackbar("MaxVal", "Cube", 236, 255, nothing)

    cube = Cube.getInstance()

    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
            detect = cube.detectFace(frame)
            cv2.imshow("Cube", detect)

            if cv2.waitKey(1) == ord("s"):
                cube.initialise()
            if cv2.waitKey(1) == ord("a"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    main()
