import numpy as np
import cv2
import os

from detection.Utils import Utils
from detection.Colors import Colors
from solver.Directions import Directions
from solver.Solver import Solver
from pynput import keyboard


class Cube:
    __instance = None

    def __init__(self):
        self.state = {
            color: np.array([[None] * 3] * 3, dtype=object) for color in Colors
        }
        self.__initialised = False
        self.stateComplete = False
        self.solvingMode = False
        self.currentFace = np.empty((3, 3), dtype=object)
        self.currentFace.fill(None)
        self.contourBoundary = None

        self.nextColor = Colors.WHITE
        self.faceColorsDetected = False
        self.listener = keyboard.Listener(on_press=self.onKeyPress)
        self.listener.start()

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Cube()
        return cls.__instance

    def getState(self) -> np.array:
        return self.state

    def resetState(self) -> None:
        self.state = {
            color: np.array([[None] * 3] * 3, dtype=object) for color in Colors
        }

    def setState(self, color, face) -> None:
        self.state[color] = face.copy()

    def isInitialised(self) -> bool:
        return self.__initialised

    def initialise(self) -> None:
        self.__initialised = True

    def getCurrentFace(self) -> np.array:
        return self.currentFace

    def getCurrentCenter(self) -> Colors:
        if self.faceColorsDetected:
            return self.currentFace[1][1]
        return None

    def getContourBoundary(self):
        return self.contourBoundary

    def isStateComplete(self):
        return self.stateComplete

    def isSolvingMode(self):
        return self.solvingMode

    def setContourBoundary(self, contour) -> None:
        self.contourBoundary = contour

    def getNextColor(self) -> Colors:
        return self.nextColor

    def setNextColor(self, color) -> None:
        self.nextColor = color

    def update(self, img) -> None:
        if not self.isInitialised():
            Utils.write(
                img,
                f"Show White face with Orange on top then press Enter to start.",
                (10, 30),
                (0, 0, 0),
            )
            return img

        elif self.isStateComplete():
            if self.getCurrentCenter() is not Colors.WHITE and not self.isSolvingMode():
                nextDir = Solver.getNextMoveToBuildState(
                    self.getState(), self.getCurrentCenter()
                )
                Utils.arrows(img, self.getContourBoundary(), dir=nextDir)
                Utils.write(img, "Face Towards White", (10, 30), (0, 0, 0))
            else:
                self.solvingMode = True
                Utils.write(
                    img,
                    f"Solution Algorithm:",
                    (10, 30),
                    (0, 0, 200),
                )
                Utils.write(
                    img,
                    f"{Solver.generateCubeString(self.state)}",
                    (10, 70),
                    (0, 0, 0),
                )

        elif self.getCurrentCenter() is self.getNextColor():
            Utils.write(img, "Press space to save.", (10, 30), (0, 0, 0))

        elif not self.isStateComplete():
            Utils.write(img, f"Show {self.getNextColor()} face", (10, 30), (0, 0, 0))
            nextDir = Solver.getNextMoveToBuildState(
                self.getState(), self.getCurrentCenter()
            )
            Utils.arrows(img, self.getContourBoundary(), dir=nextDir)

        Utils.write(img, "Press R to reset.", (10, img.shape[0] - 20), (0, 0, 200))

        return self.detectFace(img)

    def detectFace(self, img) -> None:
        if self.isSolvingMode():
            return img
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
        # cv2.imshow("thresh", thresh)
        if len(contours) > 0:
            # Draw bounding box on largest contour
            contourBoundary = cv2.boundingRect(contours[0])
            x, y, w, h = contourBoundary

            if abs(1 - (w / h)) < 0.1:
                # Draws the contour and tries to find the colors inside that boundary and create the cube face
                self.setContourBoundary(contourBoundary)
                self.drawFaceBoundary(detected)
                self.findCurrentFaceColors(detected)

                # if not self.faceColorsDetected:
                #     Utils.write(detected, f"No Face Detected2", (10, 70), (0, 0, 255))
                # return detected
            else:
                self.setContourBoundary(None)

        # Utils.write(detected, f"No Face Detected", (10, 70), (0, 0, 255))
        return detected

    def drawFaceBoundary(self, img) -> None:
        x, y, w, h = self.getContourBoundary()
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img

    def findCurrentFaceColors(self, img):
        x, y, w, h = self.getContourBoundary()
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

        # Extracting every color in all 9 squares
        for row in range(3):
            for col in range(3):
                self.currentFace[row][col] = Utils.extractColor(squares[row][col])

        # If there's one square undetected, whole face is compromised
        self.faceColorsDetected = all(
            square is not None for row in self.currentFace for square in row
        )

        return

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

        # Draw the skeleton
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

    def onKeyPress(self, key):
        if key == keyboard.Key.enter and not self.isInitialised():
            self.__initialised = True

        elif (
            key == keyboard.Key.space
            and self.isInitialised()
            and self.getCurrentCenter() is self.getNextColor()
        ):
            if self.faceColorsDetected:
                # Set the state of the current color to the current face being detected and setting the next color
                self.setState(self.getCurrentCenter(), self.getCurrentFace())
                if self.getNextColor().getValue() == 6:
                    self.stateComplete = True
                else:
                    self.setNextColor(Colors.getColor(self.nextColor.getValue() + 1))
        elif "char" in dir(key):
            if key.char == "r" or key.char == "R":
                self.__initialised = False
                self.stateComplete = False
                self.solvingMode = False
                self.nextColor = Colors.WHITE
                self.resetState()


def main():
    cube = Cube()
    print("hey")


if __name__ == "__main__":
    main()
