import numpy as np
import cv2
import os

imagesDir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "images"
)


class Cube:
    def __init__(self):
        self.__faces = np.zeros(shape=(6, 3, 3))
        self.initialised = False

    def getFaces(self) -> np.array:
        return self.__faces

    def nothing(self,x):
        pass
    
    def detect(self, frame) -> np.array:
        
        if not self.initialised:
            self.writeMessage(frame, "Not initialised")
        return frame

    def writeMessage(self, frame, msg):
        frame = cv2.putText(
            frame,
            msg,
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (60, 250, 100),
            3,
            cv2.LINE_AA,
        )


def displayImage(img):
    cv2.imshow("CubeSolver", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    img = cv2.imread(os.path.join(imagesDir, "blue.jpg"))
    cube = Cube()
    cube.detect(img)

    


if __name__ == "__main__":
    main()
