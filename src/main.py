import cv2
import numpy as np
from pynput import keyboard

from detection.Cube import Cube
from detection.Utils import Utils


def nothing(x):
    pass


def main():
    cap = cv2.VideoCapture(0)
    cap.open("http://192.168.1.5:8080/video")

    cv2.namedWindow("Cube")
    cube = Cube.getInstance()

    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (960, 540))
            detect = cube.update(frame)
            cv2.imshow("Cube", detect)

            # if solver:
            # solver.update(cube)
            if cv2.waitKey(1) == ord("a"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    main()
