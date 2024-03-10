from enum import Enum
import numpy as np


class Colors(Enum):
    WHITE = 0
    RED = 1
    ORANGE = 2
    YELLOW = 3
    BLUE = 4
    GREEN = 5

    def __str__(self):
        return self.name.title()
    
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
            return np.array([0, 0, 89], dtype=np.uint8)
        elif self == Colors.RED:
            return np.array([168, 90, 36], dtype=np.uint8)
        elif self == Colors.ORANGE:
            return np.array([7, 120, 95], dtype=np.uint8)
        elif self == Colors.YELLOW:
            return np.array([22, 65, 75], dtype=np.uint8)
        elif self == Colors.BLUE:
            return np.array([90, 100, 85], dtype=np.uint8)
        elif self == Colors.GREEN:
            return np.array([49, 40, 65], dtype=np.uint8)

    def getMaxRange(self) -> np.array:
        if self == Colors.WHITE:
            return np.array([145, 47, 253], dtype=np.uint8)
        elif self == Colors.RED:
            return np.array([190, 250, 236], dtype=np.uint8)
        elif self == Colors.ORANGE:
            return np.array([19, 255, 254], dtype=np.uint8)
        elif self == Colors.YELLOW:
            return np.array([37, 244, 254], dtype=np.uint8)
        elif self == Colors.BLUE:
            return np.array([123, 255, 200], dtype=np.uint8)
        elif self == Colors.GREEN:
            return np.array([83, 250, 197], dtype=np.uint8)
