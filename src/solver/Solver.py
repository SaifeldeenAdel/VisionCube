from solver.Directions import Directions
from detection.Colors import Colors


class Solver:
    def __init__(self) -> None:
        self.cubeString = ""

    @staticmethod
    def getNextMoveToBuildState(state, center) -> Directions:
        if center == Colors.WHITE:
            if state[Colors.WHITE][0][0] == None:
                return None
            elif state[Colors.ORANGE][0][0] == None:
                return Directions.DOWN
            elif state[Colors.RED][0][0] == None:
                return Directions.UP
            elif state[Colors.BLUE][0][0] == None:
                return Directions.LEFT
            elif state[Colors.GREEN][0][0] == None:
                return Directions.RIGHT
        elif center == Colors.ORANGE:
            return Directions.UP
        elif center == Colors.RED:
            return Directions.DOWN
        elif center == Colors.GREEN:
            return Directions.LEFT
        elif center == Colors.BLUE:
            return Directions.RIGHT
        elif center == Colors.YELLOW:
            return Directions.LEFT
