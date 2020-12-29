from enum import Enum
from consts import BOARD_SIZE


class SubmarineState(Enum):
    UNDETECTED = 0
    HIT = 1


class Submarine:

    def __init__(self, *locations):
        self.locations = {}
        board_height, board_width = BOARD_SIZE
        for location in locations:
            row, column = location
            if row not in range(board_height) or column not in range(board_width):
                raise ValueError("Location out of board range")
            if location in self.locations.keys():
                raise KeyError("Location given twice")
            self.locations[location] = SubmarineState.UNDETECTED

    def hit_location(self, location):
        if location in self.locations.keys():
            self.locations[location] = SubmarineState.HIT
        else:
            raise KeyError(f"This submarine doesn't exist in location {location}")

    def is_dead(self):
        for state in self.locations.values():
            if state == SubmarineState.UNDETECTED:
                return False
        return True
