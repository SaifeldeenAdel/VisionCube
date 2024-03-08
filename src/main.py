import cv2
import numpy as np

from detection.Cube import Cube
from detection.Utils import Utils


def nothing(x):
    pass


def main():
    cap = cv2.VideoCapture(0)
    cap.open("http://192.168.1.4:8080/video")
    cv2.namedWindow("Cube")
    cv2.createTrackbar("MinHue", "Cube", 19, 255, nothing)
    cv2.createTrackbar("MaxHue", "Cube", 79, 255, nothing)

    cube = Cube.getInstance()

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
        # if not cube.isInitialised():
        #     Utils.write(
        #         frame,
        #         "Place white face towards the camera. Press S to start.",
        #         (10, 50),
        #     )
        #     cv2.imshow("Cube", frame)

        # else:
        if ret:
            detect = cube.detectFace(frame)
            if cube.getCurrentFace():
                cv2.imshow("Cube", detect)
            else:
                cv2.imshow("Cube", frame)

            if cv2.waitKey(1) == ord("s"):
                cube.initialise()
            if cv2.waitKey(1) == ord("a"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    main()
