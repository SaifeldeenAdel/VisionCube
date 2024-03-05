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

    def getColorValue(self):
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