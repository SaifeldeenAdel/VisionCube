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
        image = image.copy()
        # Process image for finding contours
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 1)
        _, thresh = cv2.threshold(blur, 42, 255, cv2.THRESH_BINARY_INV)

        # Find contours and sort by area
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = sorted(contours, reverse=True, key=cv2.contourArea)

        # Draw bounding box on largest contour
        x, y, w, h = cv2.boundingRect(contours[0])
        if abs(1 - (w / h)) < 0.05:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                image,
                f"Face Detected {w/h}",
                (10, 30),
                cv2.FONT_HERSHEY_PLAIN,
                1.5,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
        else:
            cv2.putText(
                image,
                f"No Face Detected {w/h}",
                (10, 30),
                cv2.FONT_HERSHEY_PLAIN,
                1.5,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

        return image


def nothing():
    pass


def main():
    cap = cv2.VideoCapture(0)
    cap.open("http://192.168.1.2:8080/video")
    cv2.namedWindow("Utils")
    cv2.createTrackbar("MinHue", "Utils", 19, 255, nothing)
    cv2.createTrackbar("MaxHue", "Utils", 79, 255, nothing)

    while True:
        _, frame = cap.read()
        frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
        detect = Utils.detectCube(frame)

        cv2.imshow("thresh", detect)
        if cv2.waitKey(1) == ord("a"):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
