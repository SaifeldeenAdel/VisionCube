import cv2
import numpy as np


class Utils:
    @staticmethod
    def displayImage(window_name, image) -> None:
        cv2.imshow(window_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def extractColor(image, color) -> np.array:
        image = cv2.medianBlur(image, ksize=11)

        hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(
            hsvImage, np.array(color.getMinRange()), np.array(color.getMaxRange())
        )
        maskedImage = cv2.bitwise_and(image, image, mask=mask)
        return maskedImage
