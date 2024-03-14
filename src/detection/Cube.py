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
        self.currentFace = np.empty((3, 3), dtype=object)
        self.currentFace.fill(None)
        self.faceColorsDetected = False

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

        self.drawSkeleton(detected)
        if len(contours) > 0:
            # Draw bounding box on largest contour
            contourBoundary = cv2.boundingRect(contours[0])
            x, y, w, h = contourBoundary

            if abs(1 - (w / h)) < 0.2:
                self.drawFaceBoundary(detected, contourBoundary)
                self.findCurrentFaceColors(detected, contourBoundary)
                if self.faceColorsDetected:
                    Utils.write(detected, f"Colors Detected ", (10, 30), (0, 255, 00))
                return detected

        Utils.write(detected, f"No Face Detected", (10, 30), (0, 0, 255))
        # self.currentFace = None
        return detected

    def drawFaceBoundary(self, img, contour) -> None:
        x, y, w, h = contour
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img

    def findCurrentFaceColors(self, img, contourBoundary):
        x, y, w, h = contourBoundary
        imgCopy = img.copy()

        # 9 positions for all 9 squares
        positions = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (0, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]

        # Initializing squares array which will hold image chunks
        squareSize = min(w, h) // 3
        squares = np.empty((3, 3), dtype=object)

        centerX, centerY = (x + (w // 2), y + (h // 2))

        # Extract chunks of the image for all 9 squares and draw white dots
        for i, (dx, dy) in enumerate(positions):
            x, y = centerX + dx * squareSize, centerY + dy * squareSize
            row, col = i // 3, i % 3
            squares[row][col] = imgCopy[y - 10 : y + 10, x - 10 : x + 10]
            cv2.circle(img, (x, y), 2, (255, 255, 255), -1)

        # Iterating over all colors to find the right one
        for row in range(3):
            for col in range(3):
                for color in Colors:
                    if Utils.extractColor(squares[row][col], color):
                        self.currentFace[row][col] = color
                        break
                else:
                    self.currentFace[row][col] = None

        # Utils.write(img, f"Get better lighting", (10, 70), (255, 255, 255))
        return None

    def drawSkeleton(self, img) -> None:
        h, w, d = img.shape
        black = (0, 0, 0)
        border = (125, 125, 125)

        # Calculating my square sizes
        skeletonSize = 150
        squareSize = skeletonSize // 3

        # Getting the starting point
        topLeftX = w - 180
        topLeftY = 30

        self.faceColorsDetected = all(
            square is not None for row in self.currentFace for square in row
        )

        # Draw the Rubik's Cube face
        for i in range(3):
            for j in range(3):
                # Calculate the coordinates of the square
                x1 = topLeftX + squareSize * j
                y1 = topLeftY + squareSize * i
                x2 = x1 + squareSize
                y2 = y1 + squareSize

                color = (
                    self.currentFace[i][j].getColorValue()
                    if self.faceColorsDetected
                    else black
                )

                cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
                cv2.rectangle(img, (x1, y1), (x2, y2), border, 2)

        if self.faceColorsDetected:
            Utils.write(img, f"Center:", (10, 70), (0, 255, 0))
            Utils.write(
                img,
                f"{self.currentFace[1][1]}",
                (110, 70),
                (255, 255, 255),
            )


def main():
    print("hey")


if __name__ == "__main__":
    main()
