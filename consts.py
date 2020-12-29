from enum import Enum

DEFAULT_SUBMARINES_SIZES = (2, 3, 3, 4, 5)
BOARD_SIZE = (10, 10)
GAME_PORT = 25565
GAME_FLAG = 0xff


class AttackResult(Enum):
    MISS = 1
    HIT = 2
    KILL = 3
