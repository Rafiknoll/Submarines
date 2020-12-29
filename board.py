from enum import Enum
from utils import create_multi_dimensional_array
from exceptions import LocationOccupiedException


class LocationState(Enum):
    UNKNOWN = 0
    EMPTY = 1
    HIT = 2


class SubmarineState(Enum):
    UNDETECTED = 0
    HIT = 1


class Submarine:

    def __init__(self, *locations):
        self.locations = {}
        for location in range(len(locations)):
            self.locations[location] = SubmarineState.UNDETECTED


class BoardManager:

    BOARD_SIZE = (10, 10)

    def __init__(self):
        self.enemy_board = create_multi_dimensional_array(*self.BOARD_SIZE, LocationState.UNKNOWN)
        self.own_board = create_multi_dimensional_array(*self.BOARD_SIZE, LocationState.EMPTY)
        self.submarines = []

    def find_occupied_locations(self, *locations):
        occupied_locations = []
        for location in locations:
            if self.own_board[location[0]][location[1]] != LocationState.EMPTY:
                occupied_locations.append(location)
        return occupied_locations

    def place_submarine(self, locations):
        occupied_locations = self.find_occupied_locations(*locations)
        if len(occupied_locations) == 0:
            submarine = Submarine(*locations)
            self.submarines.append(submarine)
            for location in locations:
                self.own_board[location[0]][location[1]] = submarine
        else:
            raise LocationOccupiedException(f"Location(s) already occupied: {occupied_locations}")
