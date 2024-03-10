import numpy as np
import cv2
import os

from detection.Utils import Utils
from detection.Colors import Colors

imagesDir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "images"
)


class Cube:
    __instance = None

    def __init__(self):
        self.__faces = np.zeros(shape=(6, 3, 3))
        self.__initialised = False
        self.currentFace = None

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Cube()
        return cls.__instance

    def getFaces(self) -> np.array:
        return self.__faces

    def isInitialised(self):
        return self.__initialised

    def initialise(self):
        self.__initialised = True

    def getCurrentFace(self):
        return self.currentFace

    def detectFace(self, img) -> None:
        detected = img.copy()
        # Process img for finding contours
        gray = cv2.cvtColor(detected, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 1)

        _, thresh = cv2.threshold(
            blur, 70, 255, cv2.THRESH_BINARY_INV
        )  # Change from 55-70

        # Find contours and sort by area
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = sorted(contours, reverse=True, key=cv2.contourArea)

        if len(contours) > 0:
            # Draw bounding box on largest contour
            contourBoundary = cv2.boundingRect(contours[0])
            x, y, w, h = contourBoundary

            if abs(1 - (w / h)) < 0.2:
                Utils.write(detected, f"Face Detected {w/h}", (10, 30), (0, 255, 00))
                self.__drawFaceBoundary(detected, contourBoundary)
                self.currentFace = self.findFaceColor(detected, contourBoundary)
                return detected

        Utils.write(detected, f"No Face Detected", (10, 30), (0, 0, 255))
        self.currentFace = None
        return detected

    def __drawFaceBoundary(self, img, contour) -> None:
        x, y, w, h = contour
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img

    def findFaceColor(self, img, contourBoundary):
        x, y, w, h = contourBoundary
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Getting central coordinates and getting a chunk out of the center
        centerX, centerY = (x + (w // 2), y + (h // 2))
        center = img.copy()[
            centerY - 10 : centerY + 10,
            centerX - 10 : centerX + 10,
        ]

        cv2.rectangle(
            img,
            (centerX - 1, centerY - 1),
            (centerX + 1, centerY + 1),
            (255, 255, 255),
            2,
        )

        # Iterating over all colors to find the right one
        for color in Colors:
            if Utils.extractColor(center, color):
                Utils.write(img, f"Current Face: {color}", (10, 70), (255, 255, 255))
                return color
        Utils.write(img, f"Get better lighting", (10, 70), (255, 255, 255))
        return None


def main():
    print("hey")


if __name__ == "__main__":
    main()
