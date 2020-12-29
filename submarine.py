from enum import Enum


class SubmarineState(Enum):
    UNDETECTED = 0
    HIT = 1


class Submarine:

    def __init__(self, *locations):
        self.locations = {}
        for location in range(len(locations)):
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
