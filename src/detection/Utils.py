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
        image = cv2.medianBlur(image, ksize=3)

        hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(
            hsvImage, np.array(color.getMinRange()), np.array(color.getMaxRange())
        )
        maskedImage = cv2.bitwise_and(image, image, mask=mask)
        return maskedImage

    @staticmethod
    def write(frame, msg, org):
        cv2.putText(
            frame, msg, org, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_8
        )


def nothing():
    pass


def main():
    pass


if __name__ == "__main__":
    main()
