import cv2
import numpy as np
from detection.Colors import Colors


class Utils:
    @staticmethod
    def displayImage(window_name, image) -> None:
        cv2.imshow(window_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

    @staticmethod
    def extractColor(image) -> Colors:
        image = cv2.medianBlur(image, ksize=3)

        hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        for color in Colors:
            mask = cv2.inRange(
                hsvImage, np.array(color.getMinRange()), np.array(color.getMaxRange())
            )
            # maskedImage = cv2.bitwise_and(image, image, mask=mask)
            if np.count_nonzero(mask == 255) > 150:
                return color

        return None

    @staticmethod
    def write(frame, msg, org, color):
        cv2.putText(
            frame,
            msg,
            org,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2,
            cv2.LINE_8,
        )


def nothing():
    pass


def main():
    pass


if __name__ == "__main__":
    main()
