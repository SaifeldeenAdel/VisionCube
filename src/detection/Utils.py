import cv2
import numpy as np


class Utils:
    @staticmethod
    def displayImage(window_name, image) -> None:
        cv2.imshow(window_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

    @staticmethod
    def extractColor(image, color) -> np.array:
        image = cv2.medianBlur(image, ksize=11)

        hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(
            hsvImage, np.array(color.getMinRange()), np.array(color.getMaxRange())
        )
        maskedImage = cv2.bitwise_and(image, image, mask=mask)
        return maskedImage

    def detectCube(image) -> np.array:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 1)
        min = cv2.getTrackbarPos("MinHue", "thresh")
        max = cv2.getTrackbarPos("MaxHue", "thresh")

        edges = cv2.Canny(blur, min, max)
        contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for i, cnt in enumerate(contours):
            # if the contour has no other contours inside of it
            epsilon = 0.15 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            if cv2.contourArea(cnt) > 10000:
                print(cv2.contourArea(cnt))
                cv2.drawContours(image, [cnt], 0, (0, 100, 200), -1)

            # if hierarchy[0][i][2] == -1:
            if len(approx) == 4 and cv2.contourArea(cnt) > 4000:
                cv2.drawContours(image, [cnt], 0, (0, 255, 200), -1)

        # cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        return edges


def nothing():
    pass


def main():
    cap = cv2.VideoCapture(0)
    cap.open("http://192.168.1.2:8080/video")
    cv2.namedWindow("thresh")
    cv2.createTrackbar("MinHue", "thresh", 19, 255, nothing)
    cv2.createTrackbar("MaxHue", "thresh", 79, 255, nothing)

    while True:
        _, frame = cap.read()
        frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
        yellow = Utils.detectCube(frame)

        cv2.imshow("thresh", yellow)
        cv2.imshow("og", frame)
        if cv2.waitKey(1) == ord("a"):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
