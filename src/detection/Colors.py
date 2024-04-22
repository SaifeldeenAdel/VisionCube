from enum import Enum
import numpy as np


class Colors(Enum):
    WHITE = (1, "F")
    ORANGE = (2, "U")
    RED = (3, "D")
    BLUE = (4, "R")
    GREEN = (5, "L")
    YELLOW = (6, "B")

    def __repr__(self) -> str:
        super().__repr__()
        return self.name.title()

    def __str__(self) -> str:
        super().__str__()
        return self.name.title()

    def getValue(self):
        return self.value[0]

    def getOrient(self):
        return self.value[1]

    @classmethod
    def getColor(cls, value):
        for color in cls:
            if color.getValue() == value:
                return color
        raise ValueError("Invalid color value")

    def getColorValue(self) -> np.array:
        if self == Colors.WHITE:
            return (255, 255, 255)
        elif self == Colors.RED:
            return (0, 0, 255)
        elif self == Colors.ORANGE:
            return (0, 140, 255)
        elif self == Colors.YELLOW:
            return (0, 255, 255)
        elif self == Colors.BLUE:
            return (255, 0, 0)
        elif self == Colors.GREEN:
            return (0, 200, 0)

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
