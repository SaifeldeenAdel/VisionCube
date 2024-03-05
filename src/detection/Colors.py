from enum import Enum
import numpy as np


class Colors(Enum):
    WHITE = 0
    RED = 1
    ORANGE = 2
    YELLOW = 3
    BLUE = 4
    GREEN = 5

    def oppositeColor(self):
        if self == Colors.WHITE:
            return Colors.YELLOW
        elif self == Colors.RED:
            return Colors.ORANGE
        elif self == Colors.ORANGE:
            return Colors.RED
        elif self == Colors.YELLOW:
            return Colors.WHITE
        elif self == Colors.BLUE:
            return Colors.GREEN
        elif self == Colors.GREEN:
            return Colors.BLUE

    def getColorValue(self) -> np.array:
        if self == Colors.WHITE:
            return np.array([255, 255, 255], dtype=np.uint8)
        elif self == Colors.RED:
            return np.array([255, 0, 0], dtype=np.uint8)
        elif self == Colors.ORANGE:
            return np.array([255, 165, 0], dtype=np.uint8)
        elif self == Colors.YELLOW:
            return np.array([255, 255, 0], dtype=np.uint8)
        elif self == Colors.BLUE:
            return np.array([0, 0, 255], dtype=np.uint8)
        elif self == Colors.GREEN:
            return np.array([0, 128, 0], dtype=np.uint8)

    def getMinRange(self) -> np.array:
        if self == Colors.WHITE:
            return np.array([0, 0, 145], dtype=np.uint8)
        elif self == Colors.RED:
            return np.array([0, 99, 70], dtype=np.uint8)
        elif self == Colors.ORANGE:
            return np.array([9, 120, 106], dtype=np.uint8)
        elif self == Colors.YELLOW:
            return np.array([24, 93, 115], dtype=np.uint8)
        elif self == Colors.BLUE:
            return np.array([90, 125, 125], dtype=np.uint8)
        elif self == Colors.GREEN:
            return np.array([49, 40, 109], dtype=np.uint8)

    def getMaxRange(self) -> np.array:
        if self == Colors.WHITE:
            return np.array([179, 49, 240], dtype=np.uint8)
        elif self == Colors.RED:
            return np.array([9, 226, 236], dtype=np.uint8)
        elif self == Colors.ORANGE:
            return np.array([19, 244, 255], dtype=np.uint8)
        elif self == Colors.YELLOW:
            return np.array([40, 245, 255], dtype=np.uint8)
        elif self == Colors.BLUE:
            return np.array([115, 255, 255], dtype=np.uint8)
        elif self == Colors.GREEN:
            return np.array([83, 203, 183], dtype=np.uint8)
    
