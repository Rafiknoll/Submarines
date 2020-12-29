from enum import Enum
from submarine import Submarine
from utils import create_multi_dimensional_array
from exceptions import LocationOccupiedException
from consts import BOARD_SIZE, AttackResult


class LocationState(Enum):
    UNKNOWN = 0
    EMPTY = 1
    HIT = 2


class BoardManager:

    def __init__(self):
        self.enemy_board = create_multi_dimensional_array(*BOARD_SIZE, default_value=LocationState.UNKNOWN)
        self.own_board = create_multi_dimensional_array(*BOARD_SIZE, default_value=LocationState.EMPTY)
        self.submarines = []
        self.submarines_to_sink = 0

    def find_occupied_locations(self, *locations):
        occupied_locations = []
        for location in locations:
            row, column = location
            if self.own_board[row][column] != LocationState.EMPTY:
                occupied_locations.append(location)
        return occupied_locations

    def place_submarine(self, locations):
        occupied_locations = self.find_occupied_locations(*locations)
        if len(occupied_locations) == 0:
            submarine = Submarine(*locations)
            self.submarines.append(submarine)
            for location in locations:
                row, column = location
                self.own_board[row][column] = submarine
            self.submarines_to_sink += 1  # It is logical that for each submarine we have, the other person has one
        else:
            raise LocationOccupiedException(f"Location(s) already occupied: {occupied_locations}")

    def get_result_of_being_attacked(self, location):
        row, column = location
        try:
            if self.own_board[row][column] in [LocationState.EMPTY, LocationState.HIT]:
                return AttackResult.MISS
        except IndexError:
            return AttackResult.MISS

        hit_submarine = self.own_board[row][column]
        hit_submarine.hit_location(location)
        self.own_board[row][column] = LocationState.HIT
        if hit_submarine.is_dead():
            return AttackResult.KILL
        else:
            return AttackResult.HIT

    def save_result_of_attacking(self, location, result):
        row, column = location
        if result == AttackResult.MISS:
            self.enemy_board[row][column] = LocationState.EMPTY
        else:
            self.enemy_board[row][column] = LocationState.HIT
            if result == AttackResult.KILL:
                self.submarines_to_sink -= 1
