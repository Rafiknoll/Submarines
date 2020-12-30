"""
Name:       submarine.py

Purpose:    Provides a class to hold the information on a submarine

Usage:      from submarine import Submarine

Author:     Rafael Knoll
"""
from enum import Enum
from consts import BOARD_SIZE


class SubmarineState(Enum):
    """
    Represents the state in which each location of the submarine can be
    """
    UNDETECTED = 0
    HIT = 1


class Submarine:
    """
    Provides easy means to manage submarines and check on them
    """

    def __init__(self, *locations):
        self.locations = {}
        prev_row = None
        prev_column = None
        board_height, board_width = BOARD_SIZE
        for location in locations:
            row, column = location
            if row not in range(board_height) or column not in range(board_width):
                raise ValueError(f"Location out of board range: {location}")
            if location in self.locations.keys():
                raise KeyError(f"Location given twice: {location}")
            if prev_row is not None and prev_column is not None and not (
                    (abs(row-prev_row) == 0 and abs(column-prev_column) == 1) or
                    (abs(row-prev_row) == 1 and abs(column-prev_column) == 0)):
                raise ValueError(f"Locations are not neighbouring: {(row, column)} and {(prev_row, prev_column)}")
            self.locations[location] = SubmarineState.UNDETECTED
            prev_row, prev_column = location

    def hit_location(self, location):
        """
        Hits the target location of the submarine
        :param location: The location to hit
        :return: None
        :raises: KeyError if this location is not on the submarine
        """
        if location in self.locations.keys():
            self.locations[location] = SubmarineState.HIT
        else:
            raise KeyError(f"This submarine doesn't exist in location {location}")

    def is_dead(self):
        """
        Checks if the submarine is dead
        :return: True if it is dead
        """
        for state in self.locations.values():
            if state == SubmarineState.UNDETECTED:
                return False
        return True
